from rest_framework import serializers
from .models import Movies, TVShows, Seasons, Episodes

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'

class TVShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVShows
        fields = '__all__'

class SeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields = '__all__'

class EpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodes
        fields = '__all__'