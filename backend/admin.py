from django.contrib import admin
from .models import ChampionRating


class MLMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'rel_rate', 'id', 'role', 'patch')


# Register your models here.

admin.site.register(ChampionRating, MLMetaAdmin)
