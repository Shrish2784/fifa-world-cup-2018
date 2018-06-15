class Match(object):
    def __init__(self, home_team, away_team, home_team_goal, away_team_goal, date):
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_goal = home_team_goal
        self.away_team_goal = away_team_goal
        self.date = date


class PastMatch(Match):

    def __init__(self, home_team, away_team, home_team_goal, away_team_goal, date):
        super.__init__(home_team, away_team, home_team_goal, away_team_goal, date)
        self.winner = self._get_winner(home_team, away_team, home_team_goal, away_team_goal)

    def _get_winner(self, home_team, away_team, home_team_goal, away_team_goal):
        if home_team_goal > away_team_goal:
            return home_team
        elif away_team_goal < home_team_goal:
            return away_team
        else:
            return "Tie"


class CurrentMatch(Match):
    def __init__(self, home_team, away_team, home_team_goal, away_team_goal, date, time, home_team_event,
                 away_team_event):
        super.__init__(home_team, away_team, home_team_goal, away_team_goal, date)
        self.time = time
        self.home_team_event = home_team_event
        self.away_team_event = away_team_event
