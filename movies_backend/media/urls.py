from django.urls import path
from . import views

urlpatterns = [
    path('add_movie/', views.add_movie, name='add_movie'),
    path('get_movie/', views.get_movie, name='get_movie'),
    path('add_tv_show/', views.add_tv_show, name='add_tv_show'),
    path('get_tv_show/', views.get_tv_show, name='get_tv_show'),
    path('get_media_titles/', views.get_media_titles, name='get_media_titles'),
    path('add_server/', views.add_server, name='add_server'),
    path('get_movie_data/', views.get_movie_data, name='get_movie_data'),    
    path('get_tv_show_data/', views.get_tv_show_data, name='get_tv_show_data'),
]