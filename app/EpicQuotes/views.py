import requests
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404
from .openai import OpenAI
from . import forms
from . import models


class MovieNotFoundException(Exception):
    pass


class DashboardView(FormView):
    template_name = "EpicQuotes/Dashboard/index.html"
    form_class = forms.SelectMovieForm

    def get_success_url(self):
        return reverse_lazy(
            'movie_detail',
            kwargs={'imdb_id': self.kwargs["imdb_id"]}
        )

    def form_valid(self, form):
        try:
            movie = self.fetch_movie_from_api(form.cleaned_data['movie_title'])
            self.kwargs['imdb_id'] = movie.imdb_id
        except MovieNotFoundException:
            form.add_error('movie_title', 'Movie not found')
            return self.form_invalid(form)
        try:
            quote = OpenAI.perform_quote_prompting(movie)
            quote_background = OpenAI.perform_background_prompting(movie, quote)
        except Exception as e:
            form.add_error(None, 'Some Failure occurred during prompting.')
            return self.form_invalid(form)
        models.Quote.objects.create(
            movie=movie,
            body=quote,
            background=quote_background,
        )
        return super().form_valid(form)

    def fetch_movie_from_api(self, title):
        response = requests.get(
            "http://www.omdbapi.com/",
            params={
                "t": title,
                "apikey": settings.OMDB_API_KEY,
            }
        )
        data = response.json()
        if 'Error' in data:
            raise MovieNotFoundException
        try:
            year = int(data['Year'])
        except ValueError:
            year = None
        try:
            movie = models.Movie.objects.get(imdb_id=data['imdbID'])
        except models.Movie.DoesNotExist:
            movie = models.Movie.objects.create(
                imdb_id=data['imdbID'],
                title=data['Title'],
                year=year,
                poster_url=data['Poster'],
                actors=data['Actors'],
            )
        return movie


class MovieDetailView(TemplateView):
    template_name = "EpicQuotes/MovieDetail/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = get_object_or_404(models.Movie, imdb_id=kwargs['imdb_id'])
        quote = context['movie'].quotes.last()
        context['quote'] = quote
        return context
