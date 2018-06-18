import pytz
from django.http import HttpResponse
from . import models
from .model import datamodels
import datetime
import json
import requests
url = 'http://worldcup.sfg.io/matches/{}'


def index_temp(request):
    # #PAST#
    past_matches_queryset = models.PastMatchModel.objects.all()
    if len(past_matches_queryset) > 0:
        data = past_matches_queryset.order_by("-id")[0].matches
        past_matches = {
            'type': 'past',
            'fixtures': json.loads(data)
        }
    else:
        past_matches = {}

    # #PRESENT#
    current_matches_queryset = models.CurrentMatchModel.objects.all()
    validation_result = validate_data(current_matches_queryset)
    if validation_result['status']:
        match_object = datamodels.CurrentMatch(**validation_result['match_object'][0])
        data = match_object.__dict__
        current_matches = {
            'type': 'present',
            'fixtures': data
        }
    else:
        current_matches = {}

    # #FUTURE#
    future_matches_queryset = models.FutureMatchModel.objects.all()
    if len(future_matches_queryset) > 0:
        data = future_matches_queryset.order_by("-id")[0].matches
        future_matches = {
            'type': 'future',
            'fixtures': json.loads(data)
        }
    else:
        future_matches = {}

    response = {
        {'type': 'past', 'matches': past_matches},
        {'type': 'current', 'matches': current_matches},
        {'type': 'future', 'matches': future_matches}
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


def validate_data(res):
    if len(res) > 0:
        match_details = res.order_by("-id")[0].match_details
        match_object = json.loads(match_details)
        if len(match_object) > 0:
            return {'status': True, 'match_object': match_object}
    return {'status': False}


def index(request):
    """
    Response cgiving past, current, future depending upon circumstances.

    """
    response = models.CurrentMatchModel.objects.all()
    result = validate_data(response)
    if result['status']:
        match_object = datamodels.CurrentMatch(**result['match_object'][0])
        data = match_object.__dict__
        res = {
            'type': 'present',
            'fixtures': data
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        date = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)

        if date.hour < 12:
            response = models.PastMatchModel.objects.all()
            if len(response) > 0:
                data = response.order_by("-id")[0].matches
                res = {
                    'type': 'past',
                    'fixtures': json.loads(data)
                }
                return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            response = models.FutureMatchModel.objects.all()
            if len(response) > 0:
                data = response.order_by("-id")[0].matches
                res = {
                    'type': 'future',
                    'fixtures': json.loads(data)
                }
                return HttpResponse(json.dumps(res), content_type='application/json')
    dict = {}
    dict['error'] = "No data to provide!"
    return HttpResponse(json.dumps(dict), content_type='application/json')

#Test past matches response
def past_match_response(request):
    response = models.PastMatchModel.objects.all()
    if len(response) > 0:
        data = response.order_by("-id")[0].matches
        res = {
            'type': 'past',
            'fixtures': json.loads(data)
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        res = {
            'type': 'past',
            'fixtures': 'Not Available'
        }
        return HttpResponse(json.dumps(res), content_type='application/json')

#Test current matches response
def current_match_response(request):
    response = models.CurrentMatchModel.objects.all()
    result = validate_data(response)
    if result['status']:
        match_object = datamodels.CurrentMatch(**result['match_object'][0])
        data = match_object.__dict__
        res = {
            'type': 'present',
            'fixtures': data
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        res = {
            'type': 'current',
            'fixtures': 'Not Available'
        }
        return HttpResponse(json.dumps(res), content_type='application/json')

#Test future matches response
def future_match_response(request):
    response = models.FutureMatchModel.objects.all()
    if len(response) > 0:
        data = response.order_by("-id")[0].matches
        res = {
            'type': 'future',
            'fixtures': json.loads(data)
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        res = {
            'type': 'future',
            'fixtures': 'Not Available'
        }
        return HttpResponse(json.dumps(res), content_type='application/json')

#Sync current matches
def sync_current_match(request):
    res = requests.get(url.format('current')).json()
    model = models.CurrentMatchModel.objects.create(match_details=json.dumps(res))
    model.save()

    models.CurrentMatchModel.objects.exclude(id=model.id).delete()
    print(model.__dict__)
    return HttpResponse("Success")

#Sync all the other matches
def sync_matches(request):
    completed = []
    future = []
    n_completed_matches = 0
    matches = requests.get(url.format('?by_date=asc')).json()

    matches = sorted(matches, key=lambda x: x['datetime'])

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
        print(completed[i])

    model = models.PastMatchModel.objects.create(matches=json.dumps(completed))
    model.save()
    models.PastMatchModel.objects.exclude(id=model.id).delete()

    model = models.FutureMatchModel.objects.create(matches=json.dumps(future))
    model.save()
    models.FutureMatchModel.objects.exclude(id=model.id).delete()
    return HttpResponse("success")
