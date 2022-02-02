from django.db import models


class ChampionRating(models.Model):
    name = models.CharField(max_length=120)
    rel_rate = models.FloatField()
    patch = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    id = models.CharField(max_length=120, primary_key=True)

    def _str_(self):
        return self.id + " " + self.rel_rate
