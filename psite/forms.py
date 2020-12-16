from django import forms


class PoetryForm(forms.Form):
    poetry_seed = forms.CharField(label='Poetry seed')
    n_words = forms.IntegerField()