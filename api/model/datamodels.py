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
        'goal': 'goal_scored.png',
        'goal-own': 'own_goal.png',
        'goal-penalty': 'penalty_miss.png',
        'red-card': 'straight_red_card.png',
        'yellow-card': 'yellow.png',
        'yellow-card-second': 'second_yellow_card.png',
        'substitution-in': 'substitution.png',
        'substitution-in halftime': 'substitution.png'
    }

    def __init__(self, home_team, away_team, datetime, winner, time, home_team_events,
                 away_team_events, **kwargs):

        self.time = time
        self.home_team_event = self.get_event(home_team_events)
        self.away_team_event = self.get_event(away_team_events)

        super().__init__(home_team, away_team, datetime, winner, **kwargs)

    def get_event(self, events):
        if len(events) > 0:
            event = events[-1]

            last_name = list(event['player'].split(" "))
            last_name = last_name[-1]

            event_object = {
                'event_text': last_name + "  " + event['time'],
                'event_icon_filename': self.event_to_icon[event['type_of_event']]
            }
        else:
            event_object = None

        return event_object
