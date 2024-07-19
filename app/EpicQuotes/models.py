from django.db import models


class Movie(models.Model):
    imdb_id = models.CharField(
        max_length=20,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        max_length=240,
    )
    year = models.IntegerField(
        null=True,
    )
    poster_url = models.URLField(
        null=True,
        blank=True,
    )
    actors = models.CharField(
        max_length=2056,
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.title} - {self.year}"


class Quote(models.Model):
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name='quotes',
    )
    body = models.TextField()
    background = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.movie.title} - {self.body[:50]}"
