from rest_framework import serializers
from .models import Movies, TVShows, Seasons, Episodes

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'



class EpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodes
        fields = '__all__'

    def create(self, validated_data):
        episode = Episodes.objects.create(**validated_data)
    
        return episode


class SeasonsSerializer(serializers.ModelSerializer):
    episodes = EpisodesSerializer(many=True)

    class Meta:
        model = Seasons
        fields = ['season_number', 'episodes']
    
    def create(self, validated_data):
        season = Seasons.objects.create(**validated_data)
    
        return season


class TVShowsSerializer(serializers.ModelSerializer):
    seasons = SeasonsSerializer(many=True)

    class Meta:
        model = TVShows
        fields = ['title', 'imdb_id', 'tmdb_id', 'description', 'image', 'seasons']
        
    def create(self, validated_data):

        seasons_data = validated_data.pop('seasons')
        print(seasons_data)
        print()
        tv_show = TVShows.objects.create(**validated_data)
        for season_data in seasons_data:
            episodes_data = season_data.pop('episodes')
            season = Seasons.objects.create(tv_show=tv_show, **season_data)

            for episode_data in episodes_data:
                Episodes.objects.create(season=season, **episode_data)
            
        return tv_show
    

