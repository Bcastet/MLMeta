from rest_framework import serializers
from .models import ChampionRating


class ChampionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionRating
        fields = ('name', 'rel_rate', 'id', 'role', 'patch')

