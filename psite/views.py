from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import os
import markovify

from .forms import PoetryForm


data = open('corpora/christmas.txt',encoding="utf8").read()
corpus = data.lower().split("\n")


# Create your views here.
def index(request):
    return render(request, 'index.html')


def generate(request):
    print('You have reached me')

    if request.method == 'POST':
        form = PoetryForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/poetry', {'form': form})

    # If no entry we just assume some default values
    form = PoetryForm()
    form.poetry_seed = 'Yonder window breaks'
    form.n_words = 60

    # model here
    text_model = markovify.NewlineText(corpus)
    poem = make_song(text_model)



    return render(request, 'poetry.html', {'poem': poem})
    # return HttpResponseRedirect('/poetry', {'form': form})


def poetry(request):
    print("poetry function")

    # poetry_seed = request.poetry_seed
    # n_words = request.n_words
    # print(poetry_seed, n_words)

    return render(request, 'poetry.html')


def make_stanza(lyrics_generator):
    stanza = []
    for _ in range(4):
        while True:
            line = lyrics_generator.make_sentence()
            if line is not None:
                stanza.append(line)
                stanza.append("\n")
                break
    return stanza

def make_song(lyrics_generator):
    chorus = make_stanza(lyrics_generator)

    song = [make_stanza(lyrics_generator), "\n",
            ['CHORUS:'], chorus, "\n",
            make_stanza(lyrics_generator), "\n",
            ['CHORUS:'], chorus, "\n",
            make_stanza(lyrics_generator)]

    flat_song = [item for sublist in song for item in sublist]
    return  flat_song #os.linesep.join(song)