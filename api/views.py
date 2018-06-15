from django.shortcuts import render
from django.http import HttpResponse
from .  import models
import requests



# Create your views here.
def index(request):
    url = 'http://worldcup.sfg.io/matches/current'
    res = requests.get(url).json()

    return HttpResponse(res[0])
