from apscheduler.schedulers.blocking import BlockingScheduler
from . import models

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=.1)
def timed_job():
    url = 'http://worldcup.sfg.io/matches'
    res = requests.get(url).json()

    objects = models.Match.objects.all().delete()

    model = models.Match.objects.create(match=res)
    model.save()

sched.start()
