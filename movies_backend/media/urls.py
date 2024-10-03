from django.urls import path
from . import views

urlpatterns = [
    path('add_movie', views.add_movie, name='add_movie'),
    path('get_movies', views.get_movies, name='get_movies'),
    path('add_tv_show', views.add_tv_show, name='add_tv_show'),
    path('get_tv_shows', views.get_tv_shows, name='get_tv_shows'),
]