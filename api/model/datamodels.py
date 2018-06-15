class Match():
    def __init__(self, home_team, away_team, datetime, winner, **kwargs):
        self.home_team = home_team
        self.away_team = away_team
        self.datetime = datetime
        self.winner = winner


class PastMatch(Match):

    def __init__(self, home_team, away_team, datetime, winner, **kwargs):
        super().__init__(home_team, away_team, datetime, winner, **kwargs)


class CurrentMatch(Match):
    def __init__(self, home_team, away_team, datetime, time, winner, home_team_events,
                 away_team_events, **kwargs):
        super().__init__(home_team, away_team, datetime, winner, **kwargs)
        self.time = time
        self.home_team_event = home_team_events[-1]
        self.away_team_event = away_team_events[-1]
