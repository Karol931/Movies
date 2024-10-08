from django.db import models

# Create your models here.

class Movies(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    imdb_id = models.CharField(max_length=255, unique=True, null=False)
    tmdb_id = models.CharField(max_length=255, unique=True, null=False)
    description = models.CharField(max_length=10000, null=False)
    image = models.CharField(max_length=255, null=False)

class TVShows(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    imdb_id = models.CharField(max_length=255, unique=True, null=False)
    tmdb_id = models.CharField(max_length=255, unique=True, null=False)
    description = models.CharField(max_length=10000, null=False)
    image = models.CharField(max_length=255, null=False)

class Seasons(models.Model):
    tv_show = models.ForeignKey(to=TVShows, to_field='id', related_name='seasons', on_delete=models.CASCADE, default=None)
    season_number = models.IntegerField()

class Episodes(models.Model):
    season = models.ForeignKey(to=Seasons, to_field='id', related_name='episodes', on_delete=models.CASCADE, default=None)
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)

class Servers(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    link = models.CharField(max_length=255, unique=True, null=False)