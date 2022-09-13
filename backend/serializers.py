from rest_framework import serializers
from .models import *


class ChampionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionRating
        fields = ('name', 'rel_rate', 'id', 'role', 'patch', 'games', 'winrate')


class GameSummarySerializerSoloQ(serializers.ModelSerializer):
    class Meta:
        model = GameSummarySoloQ
        fields = '__all__'


class GameSummarySerializerCompetitive(serializers.ModelSerializer):
    class Meta:
        model = GameSummaryCompetitive
        fields = '__all__'


class TeamImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = TeamImages
        fields = '__all__'


class ChampionsBuildPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionsBuildProperties
        fields = ["keystones", "first_items"]


class ChampionMatchupPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionMatchupProperties
        fields = '__all__'
