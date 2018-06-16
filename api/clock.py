from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()
url = 'https://worldcup-18.herokuapp.com/{}'


@sched.scheduled_job('interval', minutes=.1)
def sync_current_match():
    res = requests.get(url.format('sync/current_match'))
    print(res)


@sched.scheduled_job('interval', minutes=.2)
def sync_matches():
    res = requests.get(url.format('sync/matches'))
    print(res)


sched.start()
