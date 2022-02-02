from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ChampionRatingSerializer
from .models import ChampionRating


# Create your views here.

class ChampionRatingView(viewsets.ModelViewSet):
    serializer_class = ChampionRatingSerializer
    queryset = ChampionRating.objects.all()
