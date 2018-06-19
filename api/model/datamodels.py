from datetime import datetime, timedelta


class Match:

    def __init__(self, home_team, away_team, datetime, winner, **kwargs):
        self.home_team = home_team
        self.away_team = away_team
        self.datetime = self.get_time(dt=datetime)
        self.winner = winner

    def get_time(self, dt):
        fmt = '%d %B %H:%M'
        dt_object = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%Sz')
        return (dt_object + timedelta(hours=5, minutes=30)).strftime(fmt)


class CurrentMatch(Match):
    # injury.png   |Key is not
    # offside.png  |available.

    event_to_icon = {
        'goal': 'goal_scored',
        'goal-own': 'own_goal',
        'goal-penalty': 'penalty_miss',
        'red-card': 'straight_red_card',
        'yellow-card': 'yellow',
        'yellow-card-second': 'second_yellow_card',
        'substitution-in': 'substitution',
        'substitution-out': 'substitution',
        'substitution-in halftime': 'substitution',

    }

    def __init__(self, home_team, away_team, datetime, winner, time, home_team_events,
                 away_team_events, **kwargs):

        self.time = time
        self.home_team_event = self.get_event(home_team_events)
        self.away_team_event = self.get_event(away_team_events)

        super().__init__(home_team, away_team, datetime, winner, **kwargs)

    def get_event(self, events):

        event_object = None
        if len(events) > 0:

            for i in range(len(events) - 1, -1, -1):
                event = events[i]

                if event['type_of_event'] in self.event_to_icon:

                    last_name = (list(event['player'].split(" ")))[-1]
                    if event['type_of_event'] == 'substitution-in' or event['type_of_event'] == 'substitution-in halftime':
                        event_text = "[In]" + last_name + "  " + event['time']
                    elif event['type_of_event'] == 'substitution-out':
                        event_text = "[Out]" + last_name + "  " + event['time']
                    else:
                        event_text = last_name + "  " + event['time']

                    event_object = {
                        'event_text': event_text,
                        'event_icon_filename': self.event_to_icon[event['type_of_event']]
                    }

                    break

        return event_object
