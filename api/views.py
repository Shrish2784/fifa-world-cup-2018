import pytz
from django.http import HttpResponse
from . import models
from .model import datamodels
import datetime
import json
import requests

url = 'http://worldcup.sfg.io/matches/{}'


def validate_data(res):
    if len(res) > 0:
        match_details = res.order_by("-id")[0].match_details
        match_json = json.loads(match_details)
        if len(match_json) > 0:
            return {'status': True, 'match_json': match_json}
    return {'status': False}


def index(request):
    response = models.CurrentMatchModel.objects.all()
    result = validate_data(response)
    if result['status']:
        match_object = datamodels.CurrentMatch(**result['match_json'][0])
        data = match_object.__dict__
        res = {
            'type': 'present',
            'fixtures': data
        }
        return HttpResponse(json.dumps(res))
    else:
        date = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)

        if date.hour <= 13:
            response = models.PastMatchModel.objects.all()
            if len(response) > 0:
                data = response.order_by("-id")[0].matches
                res = {
                    'type': 'past',
                    'fixtures': json.loads(data)
                }
                return HttpResponse(json.dumps(res))
        else:
            response = models.FutureMatchModel.objects.all()
            if len(response) > 0:
                data = response.order_by("-id")[0].matches
                res = {
                    'type': 'future',
                    'fixtures': json.loads(data)
                }
                return HttpResponse(json.dumps(res))
    dict = {}
    dict['error'] = "No data to provide!"
    return HttpResponse(json.dumps(dict))


def sync_current_match(request):
    res = requests.get(url.format('current')).json()
    model = models.CurrentMatchModel.objects.create(match_details=json.dumps(res))
    model.save()

    models.CurrentMatchModel.objects.exclude(id=model.id).delete()
    return HttpResponse(json.dumps(model.__dict__))


def sync_matches(request):
    completed = []
    future = []
    n_completed_matches = 0
    matches = requests.get(url.format('')).json()
    print("-----------------Scheduled job sync_matches ran-----------------------")
    for match in matches:
        if match['status'] == 'completed':
            completed.append(match)
            n_completed_matches += 1
        elif match['status'] == 'future':
            future.append(datamodels.Match(**match).__dict__)
            if len(future) >= 3:
                break
    if n_completed_matches >= 3:
        completed = completed[(len(completed) - 3): len(completed)]

    for i in range(len(completed)):
        completed[i] = datamodels.Match(**completed[i]).__dict__

    model = models.PastMatchModel.objects.create(matches=json.dumps(completed))
    model.save()
    models.PastMatchModel.objects.exclude(id=model.id).delete()

    model = models.FutureMatchModel.objects.create(matches=json.dumps(future))
    model.save()
    models.FutureMatchModel.objects.exclude(id=model.id).delete()
    completed = completed+future
    response = json.dumps(completed)

    return HttpResponse(response)
