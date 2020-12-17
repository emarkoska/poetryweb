from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras import regularizers
from keras.models import load_model
import keras.utils as ku
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import markovify
import os

global max_sequence_len

data = open('shakespeare.txt',encoding="utf8").read()
corpus = data.lower().split("\n")

def train():
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)                       #Generates a vocabulary structure. The mapping of which word is which number.
    total_words = len(tokenizer.word_index) + 1

    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]      #Maps the specific line to a sequence of indices according to the fit_on_texts
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]                                                             #windows of 1-n 'grams' and append those sequences to a list
            input_sequences.append(n_gram_sequence)

    global max_sequence_len
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))  #adds 0s as padding to all previous vectors in the beginning

    predictors, label = input_sequences[:,:-1],input_sequences[:,-1]                                         #predictors are reversed sequences, and the labels are just the last word

    label = ku.to_categorical(label, num_classes=total_words)

    model = Sequential()
    model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))                                     #total_words x 100 matrix with embeddings for all words
    model.add(Bidirectional(LSTM(150, return_sequences = True)))                                     #a subset of the matrix goes in
    model.add(Dropout(0.2))
    model.add(LSTM(100))
    model.add(Dense(int(total_words/2), activation='relu', kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    print(model.summary())

    history = model.fit(predictors, label, epochs=200, verbose=1)
    model.save('poetry_generator_shakespeare.h5')

def newpoem(seed, word_count):
    max_sequence_len = 11
    model = load_model('poetry_generator_shakespeare.h5')
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)

    for _ in range(word_count):
        token_list = tokenizer.texts_to_sequences([seed])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = model.predict_classes(token_list, verbose=0)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed += " " + output_word
    print(seed)


def make_stanza(lyrics_generator):
    stanza = ""
    for _ in range(4):
        while True:
            line = lyrics_generator.make_sentence()
            if line is not None:
                stanza += (line + "\n")
                break
    return stanza

def make_song(lyrics_generator):
    chorus = make_stanza(lyrics_generator)

    song = [make_stanza(lyrics_generator),
            'CHORUS:', chorus,
            make_stanza(lyrics_generator),
            'CHORUS:', chorus,
            make_stanza(lyrics_generator)]
    return  os.linesep.join(song)




if __name__ == '__main__':

    #train()
    #newpoem("Envious love and my", 80)

    text_model = markovify.NewlineText(corpus)
    song = make_song(text_model)
    print(song)