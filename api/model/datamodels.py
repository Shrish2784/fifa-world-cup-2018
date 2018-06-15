class Match():
    def __init__(self, home_team, away_team, datetime, winner, **kwargs):
        self.home_team = home_team.country
        self.away_team = away_team.country
        self.datetime = datetime
        self.winner = winner


class PastMatch(Match):

    def __init__(self, home_team, away_team, datetime, winner, **kwargs):
        super().__init__(home_team, away_team, datetime, **kwargs)
        self.winner = winner


class CurrentMatch(Match):
    def __init__(self, home_team, away_team, home_team_goal, away_team_goal, datetime, time, home_team_events,
                 away_team_events, **kwargs):
        super().__init__(home_team, away_team, home_team_goal, away_team_goal, datetime, time, **kwargs)
        self.time = time
        self.home_team_event = home_team_events[-1]
        self.away_team_event = away_team_events[-1]
