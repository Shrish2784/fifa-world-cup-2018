from django.db import models

# Create your models here.
class Match(models.Model):
    # away_team = models.CharField(max_length=250)
    # home_team = models.CharField(max_length=250)
    # goal_home = models.IntegerField(blank=True)
    # goal_away = models.IntegerField(blank=True)

    matches = models.CharField(max_length=20000)
