from django.db import models

# Create your models here.
class Match(models.Model):
    away_team = models.CharField(max_length=250)
    home_team = models.CharField(max_length=250)
    goal_home = models.IntegerField(blank=True)
    goal_away = models.IntegerField(blank=True)

    def __str__(self):
        return self.home_team + " v/s " + self.away_team
