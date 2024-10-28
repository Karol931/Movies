from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .utils import get_movie_parameters, get_tv_show_parameters, put_imdb_or_tmdb_id_in_link, put_episode_in_link, put_season_in_link
from .serializers import MoviesSerializer, TVShowsSerializer, ServersSerializer, MediaSerializer
from .models import Movies, TVShows, Servers
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from movies_backend.exceptions import RequestDataException, TitleException, ServerNameException, ScrapingException
from movies_backend.utils import get_title_error_property, get_server_error_property, get_scraping_error_property, get_serializer_error_property, get_request_data_error_property, get_header_param


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='title of the movie to watch'),
            'server': openapi.Schema(type=openapi.TYPE_STRING, description='Server name from witch to watch'),
        }
),
responses={
    200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'movie link': 'Link for the movie'}),
    400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': get_title_error_property(),
                'server': get_server_error_property(),
                'request data': get_request_data_error_property(),
            },
            description='Bad request error details'
        ),
})
@api_view(['POST'])
@permission_classes([AllowAny])
def get_movie(request):
    title = request.data.get('title')
    server_name = request.data.get('server')

    if not title and not server_name:
        raise RequestDataException
    
    try:
        movie = Movies.objects.get(title=title)
    except:
        raise TitleException(title=title)
    
    imdb_id, tmdb_id = movie.imdb_id, movie.tmdb_id.split('-')[0]

    try:
        server_link = Servers.objects.get(name=server_name).link
    except:
        raise ServerNameException

    movie_link = put_imdb_or_tmdb_id_in_link(imdb_id, tmdb_id, server_link)

    return Response(status=200, data={'movie link': movie_link})


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'imdbId': openapi.Schema(type=openapi.TYPE_STRING, description='Id of the movie from IMDB databse'),
            'tmdbId': openapi.Schema(type=openapi.TYPE_STRING, description='Id of the movie from TMDB database'),
        }
),
manual_parameters=get_header_param(),
responses={
    200: MoviesSerializer(),
    400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'scraping': get_scraping_error_property(),
                'serializer': get_serializer_error_property(),
                'request data': get_request_data_error_property(),
            },
            description='Bad request error details'
        ),
    401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
            },)
})
@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def add_movie(request):
    
    imdb_id = request.data.get('imdbId')
    tmdb_id = request.data.get('tmdbId')
    
    if not imdb_id and not tmdb_id:
        raise RequestDataException
    
    try:
        title, img, description = get_movie_parameters(tmdb_id)
    except:
        raise ScrapingException
    
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


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the Tv show to watch'),
            'server': openapi.Schema(type=openapi.TYPE_STRING, description='Server name from witch to watch'),
            'seasonNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Season of the Tv show'),
            'episodeNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Episode of the season'),
        }
),
responses={
    200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'Tv show link': 'Link for the Tv show'}),
    400: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': get_title_error_property(),
            'server': get_server_error_property(),
            'request data': get_request_data_error_property(),
        },
        description='Bad request error details'
    ),
})
@api_view(['POST'])
@permission_classes([AllowAny])
def get_tv_show(request):
    
    title = request.data.get('title')
    server = request.data.get('serverName')
    season_number = request.data.get('seasonNumber')
    episode_number = request.data.get('episodeNumber')
    if not title and not server and not season_number and not episode_number:
        raise RequestDataException
    
    try:
        tv_show = TVShows.objects.get(title=title)
    except:
        raise TitleException(title=title)
    
    imdb_id, tmdb_id = tv_show.imdb_id, tv_show.tmdb_id.split('-')[0]

    try:
        server_link = Servers.objects.get(name=server).link
    except:
        raise ServerNameException
    
    tv_show_link = put_imdb_or_tmdb_id_in_link(imdb_id, tmdb_id, server_link)
    tv_show_link = put_season_in_link(season_number, tv_show_link)
    tv_show_link = put_episode_in_link(episode_number, tv_show_link)

    return Response(status=200, data={'Tv show link': tv_show_link})


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'imdbId': openapi.Schema(type=openapi.TYPE_STRING, description='Id of the Tv show from IMDB databse'),
            'tmdbId': openapi.Schema(type=openapi.TYPE_STRING, description='Id of the Tv show from TMDB database'),
        }
),
manual_parameters=get_header_param(),
responses={
    200: TVShowsSerializer(),
    400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'scraping': get_scraping_error_property(),
                'serializer': get_serializer_error_property(),
                'request data': get_request_data_error_property(),
            },
            description='Bad request error details'
        ),
    401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
            },)
})
@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def add_tv_show(request):
        
        imdb_id = request.data.get('imdbId')
        tmdb_id = request.data.get('tmdbId')
        
        if not imdb_id and not tmdb_id:
            raise RequestDataException

        try:
            title, img, description, seasons = get_tv_show_parameters(tmdb_id)
        except:
            raise ScrapingException
        
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

@swagger_auto_schema(method='get',
responses={
    200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            description='An array of movie titles'
        ),
})
@api_view(['GET'])
@permission_classes([AllowAny])
def get_media_titles(request):
    serializer = MediaSerializer()
    titles = serializer.get_titles()
    return Response(status=200, data=titles)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'serverLink': openapi.Schema(type=openapi.TYPE_STRING, description='General link for the service'),
            'serverName': openapi.Schema(type=openapi.TYPE_STRING, description='Name for the server'),
        }
),
manual_parameters=get_header_param(),
responses={
    200: ServersSerializer(),
    400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
               
                'serializer': get_serializer_error_property(),
                'request data': get_request_data_error_property(),
            },
            description='Bad request error details'
        ),

    401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.')
            },)
})
@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def add_server(request):
    server_link = request.data.get('serverLink')
    server_name = request.data.get('serverName')
    
    if not server_link and not server_name:
        raise RequestDataException
    
    server = {'name': server_name, 'link': server_link}
    serializer = ServersSerializer(data=server)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=400, data=serializer.errors)

    return Response(status=200, data=serializer.data)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the movie'),
        }
),
responses={
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={'movie params': 'Parameters of the movie'},
    ),
    400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='There is no media named \'title\' in the database.'),
                'request data': get_request_data_error_property(),
            },
            description='Bad request error details'
        ),
})
@api_view(['POST'])
@permission_classes([AllowAny])
def get_movie_data(request):
    title = request.data.get('title')

    if not title:
        raise RequestDataException
    
    try:
        movie = Movies.objects.get(title=title)
    except:
        raise TitleException
    
    serializer = MediaSerializer()
    params = serializer.get_movie_params(movie)
    
    return Response(status=200, data={'movie params': params})


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the Tv show'),
        }
),
responses={
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
            properties={'Tv show params': 'Parameters of the Tv show'},
    ),
    400: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='There is no media named \'title\' in the database.'),
            'request data': get_request_data_error_property(),
        },
        description='Bad request error details'
    ),
})
@api_view(['POST'])
@permission_classes([AllowAny])
def get_tv_show_data(request):
    title = request.data.get('title')
    
    if not title:
        raise RequestDataException
    
    try:
        tv_show = TVShows.objects.get(title=title)
    except:
        raise TitleException
    
    serializer = MediaSerializer()
    params = serializer.get_tv_show_params(tv_show)
    
    return Response(status=200, data={'Tv show params': params})