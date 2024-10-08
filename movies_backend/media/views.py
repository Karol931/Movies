from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import get_movie_parameters, get_tv_show_parameters, put_imdb_or_tmdb_id_in_link, put_episode_in_link, put_season_in_link
from .serializers import MoviesSerializer, TVShowsSerializer, ServersSerializer
from .models import Movies, TVShows, Servers


@api_view(['POST'])
def get_movie(request):
    movie_title = request.POST['movieTitle']
    server_name = request.POST['serverName']
    
    movie = Movies.objects.get(title=movie_title)
    movie_imdb_id, movie_tmdb_id = movie.imdb_id, movie.tmdb_id
    server_link = Servers.objects.get(name=server_name).link

    movie_link = put_imdb_or_tmdb_id_in_link(movie_imdb_id, movie_tmdb_id, server_link)

    return Response(status=200, data=movie_link)


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
    
    return Response(status=200, data=serializer.data)


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
    serializer = TVShowsSerializer(data=tv_show_data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=400, data=serializer.errors)

    return Response(status=200, data=serializer.data)


@api_view(['POST'])
def get_tv_show(request):
    tv_show_title = request.POST['tvShowTitle']
    server_name = request.POST['serverName']
    season_number = request.POST['seasonNumber']
    episode_number = request.POST['episodeNumber']
    
    tv_show = TVShows.objects.get(title=tv_show_title)
    imdb_id, tmdb_id = tv_show.imdb_id, tv_show.tmdb_id
    server_link = Servers.objects.get(name=server_name).link

    tv_show_link = put_imdb_or_tmdb_id_in_link(imdb_id, tmdb_id, server_link)
    tv_show_link = put_season_in_link(season_number, tv_show_link)
    tv_show_link = put_episode_in_link(episode_number, tv_show_link)

    return Response(status=200, data=tv_show_link)


@api_view(['GET'])
def get_media_titles(request):
    tv_shows_titles = [title for (title,) in TVShows.objects.values_list('title')]
    movies_titles = [title for (title,) in Movies.objects.values_list('title')]
    titles = tv_shows_titles + movies_titles
    
    return Response(status=200, data=titles)


@api_view(['POST'])
def add_server(request):
    server_link = request.POST['serverLink']
    server_name = request.POST['serverName']
    server = {'name': server_name, 'link': server_link}
    serializer = ServersSerializer(data=server)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=400, data=serializer.errors)

    return Response(status=200, data=serializer.data)


