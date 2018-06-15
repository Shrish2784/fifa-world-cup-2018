from django.shortcuts import render
from django.http import HttpResponse
from .  import models
import requests



# Create your views here.
def index(request):
    url = 'http://worldcup.sfg.io/matches/today'
    res = requests.get(url).json()

    away_team = res[0]['away_team']['country']
    home_team = res[0]['home_team']['country']
    goal_home = res[0]['home_team']['goals']
    goal_away = res[0]['away_team']['goals']

    model = models.Match.objects.create(away_team=away_team, home_team=home_team, goal_home=goal_home, goal_away=goal_away)
    model.save()
    return HttpResponse(res)
