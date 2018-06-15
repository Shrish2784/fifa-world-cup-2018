from apscheduler.schedulers.blocking import BlockingScheduler
from api import models
import requests
import json
from api.model import datamodels

sched = BlockingScheduler()
url = 'http://worldcup.sfg.io/matches/{}'


@sched.scheduled_job('interval', minutes=.1)
def sync_current_match():
    res = requests.get(url.format('current')).json()
    print("Scheduled job sync_current_match ran")
    model = models.CurrentMatchModel.objects.create(match_details=json.dumps(res))
    model.save()

    models.CurrentMatchModel.objects.exclude(id=model.id).delete()


@sched.scheduled_job('interval', minutes=60)
def sync_matches():
    completed = []
    future = []
    matches = requests.get(url.format('')).json()
    print("Scheduled job sync_matches ran")
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


sched.start()
