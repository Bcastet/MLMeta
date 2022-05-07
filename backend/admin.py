from django.contrib import admin
from .models import *


class MLMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'rel_rate', 'id', 'role', 'patch')


class MLMetaGameSummaries(admin.ModelAdmin):
    list_display = [field.name for field in GameSummaryCompetitive._meta.get_fields()]

class MLMetaTeamImages(admin.ModelAdmin):
    list_display = [field.name for field in TeamImages._meta.get_fields()]


# Register your models here.

admin.site.register(ChampionRating, MLMetaAdmin)
admin.site.register(GameSummaryCompetitive, MLMetaGameSummaries)
admin.site.register(TeamImages, MLMetaTeamImages)
