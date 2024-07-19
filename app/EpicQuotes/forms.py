from django import forms


class SelectMovieForm(forms.Form):
    movie_title = forms.CharField(
        label='Movie Title',
        max_length=240,
    )
