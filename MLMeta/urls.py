"""MLMeta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import *
from rest_framework import routers
from backend import views

router = routers.DefaultRouter()
router.register(r'ratings', views.ChampionRatingView, 'championRating')
router.register(r'soloQgames', views.SoloQMatchPerformanceView, 'soloQgamessummaries')
router.register(r'competitiveGames', views.CompetitiveMatchPerformanceView, 'competitiveGamesSummaries')
router.register(r'teamImages', views.TeamImagesView, 'teamImages')
router.register(r'ChampionsBuildProperties', views.ChampionsBuildPropertiesView, 'ChampionsBuildProperties')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
