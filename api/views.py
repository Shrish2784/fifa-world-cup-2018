from django.http import HttpResponse
from . import models
from .model import datamodels
from .apps import ApiConfig
import datetime
import json
import requests

url = 'http://worldcup.sfg.io/matches/{}'


def validate_data(res):
    if len(res) > 0:
        match_details = res.order_by("-id")[0].match_details
        match_object = json.loads(match_details)
        if len(match_object) > 0:
            return {'status': True, 'match_object': match_object}
    return {'status': False}


def index(request):
    """
        Response giving past, current, future matches details depending upon the time.

    """

    date = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    if 10 <= date.hour < 12:
        # PAST
        response = models.PastMatchModel.objects.all()
        if len(response) > 0:
            data = response.order_by("-id")[0].matches
            res = {
                'type': 'past',
                'show_after_minutes': 5,
                'fixtures': json.loads(data)
            }
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            # EMPTY
            return HttpResponse(json.dumps({}), content_type='application/json')

    elif 12 <= date.hour < 17:
        # EMPTY
        return HttpResponse(json.dumps({}), content_type='application/json')

    elif 17 <= date.hour < 23:
        # Current
        response = models.CurrentMatchModel.objects.all()
        result = validate_data(response)
        if result['status']:
            match_object = datamodels.CurrentMatch(**result['match_object'][0])
            data = match_object.__dict__
            res = {
                'type': 'present',
                'show_after_minutes': 2.5,
                'fixtures': data
            }
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            # Future
            # response = models.FutureMatchModel.objects.all()
            # if len(response) > 0:
            #     data = response.order_by("-id")[0].matches
            #     res = {
            #         'type': 'future',
            #         'show_after_minutes': 5,
            #         'fixtures': json.loads(data)
            #     }
            #     return HttpResponse(json.dumps(res), content_type='application/json')
            # else:
            #     return HttpResponse(json.dumps({}), content_type='application/json')
            return HttpResponse(json.dumps({}), content_type='application/json')

    else:
        # Empty
        return HttpResponse(json.dumps({}), content_type='application/json')


# Test past matches response
def past_match_response(request):
    response = models.PastMatchModel.objects.all()
    if len(response) > 0:
        data = response.order_by("-id")[0].matches
        res = {
            'type': 'past',
            'show_after_minutes': 5,
            'fixtures': json.loads(data)
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        res = {
            'type': 'past',
            'show_after_minutes': 5,
            'fixtures': 'Not Available'
        }
        return HttpResponse(json.dumps(res), content_type='application/json')


# Test current matches response
def current_match_response(request):
    match_object = [
        {
            "venue": "Brazil",
            "location": "Arena Corinthians",
            "datetime": "2018-06-18T09:43:51Z",
            "status": "in progress",
            "time": "halftime",
            "last_score_update_at": "2018-06-15T19:01:58.773Z",
            "last_event_update_at": "2018-06-15T19:01:58.773Z",
            "home_team": {
                "country": "Brazil",
                "code": "BRA",
                "goals": 3
            },
            "away_team": {
                "country": "Croatia",
                "code": "CRO",
                "goals": 1
            },
            "winner": "Brazil",

            "home_team_events": [
                {
                    "id": 11,
                    "type_of_event": "goal-own",
                    "player": "Marcelo",
                    "time": "11'"
                }
            ],
            "away_team_events": [
                {
                    "id": 23,
                    "type_of_event": "substitution-in",
                    "player": "BrozoviĆ",
                    "time": "61'"
                }
            ]
        }
    ]

    result = {'status': True, 'match_object': match_object}

    match_object = datamodels.CurrentMatch(**result['match_object'][0])
    data = match_object.__dict__
    res = {
        'type': 'present',
        'show_after_minutes': 2.5,
        'fixtures': data
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# Test future matches response
def future_match_response(request):
    response = models.FutureMatchModel.objects.all()
    if len(response) > 0:
        data = response.order_by("-id")[0].matches
        res = {
            'type': 'future',
            'show_after_minutes': 5,
            'fixtures': json.loads(data)
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        res = {
            'type': 'future',
            'show_after_minutes': 5,
            'fixtures': 'Not Available'
        }
        return HttpResponse(json.dumps(res), content_type='application/json')


# Empty Reponse
def empty_response(request):
    return HttpResponse(json.dumps({}), content_type='application/json')


# Sync current matches
def sync_current_match(request):
    res = requests.get(url.format('current')).json()
    model = models.CurrentMatchModel.objects.create(match_details=json.dumps(res))
    model.save()

    models.CurrentMatchModel.objects.exclude(id=model.id).delete()
    return HttpResponse("Success")


# Sync all the other matches
def sync_matches(request):
    t_date = (datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)).day
    completed = []
    future = []
    n_completed_matches = 0
    matches = requests.get(url.format('?by_date=asc')).json()

    matches = sorted(matches, key=lambda x: x['datetime'])

    for match in matches:
        if match['status'] == 'completed':
            completed.append(match)
            n_completed_matches += 1
        elif match['status'] == 'future':
            match_object = datamodels.Match(**match).__dict__
            m_date = datetime.datetime.strptime(match_object['datetime'], '%d %B %H:%M').day
            if m_date == t_date:
                future.append(match_object)
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
    return HttpResponse("success")
