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

    tvshow_data = {
        'imdb_id' : imdb_id,
        'tmdb_id' : tmdb_id,
        'title' : title,
        'image' : img,
        'description' : description
    }
    tv_show_serializer = TVShowsSerializer(data=tvshow_data)
    if tv_show_serializer.is_valid():
        tv_show_serializer.save()
    else:
        return Response(status=400, data=tv_show_serializer.errors)
    
    for season in seasons:
        seasons_serializer = SeasonsSerializer(data={'tv_show_id': tv_show_serializer.data['id'], 'season_number': season['season_number']})
        if seasons_serializer.is_valid():
            seasons_serializer.save()
            for episode in season['episodes']:
                episode_serializer = EpisodesSerializer(data={'season_id': seasons_serializer.data['id'], 'episode_number': episode['episode_number'], 'title': episode['title']})
                if episode_serializer.is_valid():
                    episode_serializer.save()
                else:
                    return Response(status=400, data=episode_serializer.errors)
        else:
            return Response(status=400, data=seasons_serializer.errors)

    return Response()

@api_view(['GET'])
def get_tv_shows(request):
    tv_shows = TVShows.objects.select_related("seasons").all()
    print(tv_shows.values())
    serializer = MoviesSerializer(tv_shows, many=True)
    
    return Response(serializer.data)