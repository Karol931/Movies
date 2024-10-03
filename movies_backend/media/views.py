from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import get_movie_parameters, get_tv_show_parameters
from .serializers import MoviesSerializer, TVShowsSerializer, SeasonsSerializer, EpisodesSerializer
from .models import Movies, TVShows, Seasons, Episodes


@api_view(['GET'])
def get_movies(request):
    movies = Movies.objects.all()
    serializer = MoviesSerializer(movies, many=True)
    
    return Response(serializer.data)


@api_view(['POST'])
def add_movie(request):
    imdb_id = request.POST['imdbId']
    tmdb_id = request.POST['tmdbId']
    title, img, description = get_movie_parameters(tmdb_id)
    
    data = {
        'imdb_id' : imdb_id,
        'tmdb_id' : tmdb_id,
        'title' : title,
        'image' : img,
        'description' : description
    }

    serializer = MoviesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=400, data=serializer.errors)
    
    return Response()


@api_view(['POST'])
def add_tv_show(request):
    imdb_id = request.POST['imdbId']
    tmdb_id = request.POST['tmdbId']

    title, img, description, seasons = get_tv_show_parameters(tmdb_id)

    tv_show_data = {
        'imdb_id' : imdb_id,
        'tmdb_id' : tmdb_id,
        'title' : title,
        'image' : img,
        'description' : description,
        'seasons': seasons
    }
    tv_show_serializer = TVShowsSerializer(data=tv_show_data)
    if tv_show_serializer.is_valid():
        tv_show_serializer.save()
    else:
        return Response(status=400, data=tv_show_serializer.errors)

    return Response(tv_show_serializer.data)

@api_view(['GET'])
def get_tv_shows(request):
    tv_shows = TVShows.objects.all()
    serializer = TVShowsSerializer(tv_shows, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def get_media_titles(request):
    tv_shows_titles = [title for (title,) in TVShows.objects.values_list('title')]
    movies_titles = [title for (title,) in Movies.objects.values_list('title')]
    titles = tv_shows_titles + movies_titles
    return Response(titles)
