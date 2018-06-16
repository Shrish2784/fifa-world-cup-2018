from apscheduler.schedulers.blocking import BlockingScheduler

print("----------------------Scheduled job sync_current_match Import---------------------------------")
import requests

sched = BlockingScheduler()
url = 'http://worldcup.sfg.io/matches/{}'


@sched.scheduled_job('interval', minutes=.1)
def sync_current_match():
    res = requests.get(url.format('current')).json()
    print("----------------------Scheduled job sync_current_match ran---------------------------------")
    print(res)


sched.start()
