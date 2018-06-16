from django.http import HttpResponse
from . import models
from .model import datamodels
import datetime
import json
import requests

url = 'http://worldcup.sfg.io/matches/{}'


def index(request):
    response = models.CurrentMatchModel.objects.all()
    if len(response) > 0:
        match_json = json.loads(response.order_by("-id")[0].match_details)
        print(match_json)
        match_object = datamodels.CurrentMatch(**match_json[0])
        return HttpResponse(json.dumps(match_object.__dict__))

    else:
        d = str(datetime.datetime.now())
        time = int(d[11: 13])
        if time <= 12:
            response = models.PastMatchModel.objects.all()
            if len(response) > 0:
                return HttpResponse(response.order_by("-id")[0].matches)
        else:
            response = models.FutureMatchModel.objects.all()
            if len(response) > 0:
                return HttpResponse(response.order_by("-id")[0].matches)
    dict = {}
    dict['error'] = "No data to provide!"
    print("---------------Debugging----------------------")
    return HttpResponse(json.dumps(dict))


def sync_current_match(request):
    res = requests.get(url.format('current')).json()
    print("----------------------Scheduled job sync_current_match ran---------------------------------")
    model = models.CurrentMatchModel.objects.create(match_details=json.dumps(res))
    model.save()

    models.CurrentMatchModel.objects.exclude(id=model.id).delete()
    return HttpResponse("success")


def sync_past_future_match(request):
    completed = []
    future = []
    matches = requests.get(url.format('')).json()
    print("-----------------Scheduled job sync_matches ran-----------------------")
    for match in matches:
        if match['status'] == 'completed':
            completed.append(match)
        elif match['status'] == 'future':
            match_json = json.dumps(match)
            future.append(datamodels.Match(**match_json))
            if len(future) >= 3:
                break

    completed = completed[(len(completed) - 3): len(completed)]
    for i in range(len(completed)):
        match_json = json.dumps(completed[i])
        completed[i] = datamodels.PastMatch(**match_json)

    model = models.PastMatchModel.objects.create(matches=json.dumps(completed))
    model.save()
    models.PastMatchModel.objects.exclude(id=model.id).delete()

    model = models.FutureMatchModel.objects.create(matches=json.dumps(future))
    model.save()
    models.FutureMatchModel.objects.exclude(id=model.id).delete()
    return HttpResponse("success")
