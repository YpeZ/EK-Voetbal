import pandas as pd

alphabeta = pd.read_csv('output/alphabet.csv', index_col=[0])

class Match:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

    def alphas(self):
        self.home_alpha
        return

    def home_alpha(self):
        return alphabeta.loc[self.home_team, 'alpha']

    def home_beta(self):
        return alphabeta.loc[self.home_team, 'beta']

    def away_alpha(self):
        return alphabeta.loc[self.away_team, 'alpha']

    def away_beta(self):
        return alphabeta.loc[self.away_team, 'beta']

    def matchup(self):
        home_exp = self.home_alpha() * self.away_beta()
        away_exp = self.home_beta() * self.away_alpha()
        return [home_exp, away_exp]

    def __str__(self):
        return f"{self.home_team} - {self.away_team}"


match = Match('Turkey', 'Italy')
print(match.home_team)
print(match.home_alpha())
print(match.matchup())