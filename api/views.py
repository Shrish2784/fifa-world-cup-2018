from django.shortcuts import render
from django.http import HttpResponse
from .  import models
from model import datamodels
import datetime
import json


def index(request):
    response = models.CurrentMatchModel.objects.all()
    if len(response) > 0:
        match_json =  response.order_by("-id")[0].match_details
        match_object = datamodels.CurrentMatch(**match_json)
        return json.dumps(match_object)

    else:
        d = str(datetime.datetime.now())
        time = int(d[11: 13])
        if time <= 12:
            response = models.PastMatchModel.objects.all()
            if len(response) > 0:
                return response.order_by("-id")[0].matches
        else:
            response = models.FutureMatchModel.objects.all()
            if len(response) > 0:
                return response.order_by("-id")[0].matches
    dict = {}
    dict['error'] = "No data to provide!"
    return HttpResponse(json.dumps(dict))




