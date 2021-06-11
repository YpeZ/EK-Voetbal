import pandas as pd
import numpy as np
import scipy.stats
from scipy.stats import poisson


alphabeta = pd.read_csv('output/alphabet.csv', index_col=[0])


class Match:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

        self.home_alpha = self.get_home_alpha()
        self.home_beta = self.get_home_beta()
        self.away_alpha = self.get_away_alpha()
        self.away_beta = self.get_away_beta()

        self.home_xg = self.get_home_xg()
        self.away_xg = self.get_away_xg()

        self.prob_home = self.get_prob_home()
        self.prob_draw = self.get_prob_draw()
        self.prob_away = self.get_prob_away()

    def get_home_alpha(self):
        return alphabeta.loc[self.home_team, 'alpha']

    def get_home_beta(self):
        return alphabeta.loc[self.home_team, 'beta']

    def get_away_alpha(self):
        return alphabeta.loc[self.away_team, 'alpha']

    def get_away_beta(self):
        return alphabeta.loc[self.away_team, 'beta']

    def matchup(self):
        home_exp = self.home_alpha * self.away_beta
        away_exp = self.home_beta * self.away_alpha
        return [home_exp, away_exp]

    def get_home_xg(self):
        home_xg = self.home_alpha * self.away_beta
        return home_xg

    def get_away_xg(self):
        away_xg = self.home_beta * self.away_alpha
        return away_xg

    def get_prob_home(self):
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        home = sum(poisson.pmf(k, mu_1) * poisson.cdf(k - 1, mu_2) for k in range(10))
        return home

    def get_prob_draw(self):
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        draw = sum(poisson.pmf(k, mu_1) * poisson.pmf(k, mu_2) for k in range(10))
        return draw

    def get_prob_away(self):
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        away = sum(poisson.pmf(k, mu_2) * poisson.cdf(k - 1, mu_1) for k in range(10))
        return away

    def simulate_home(self, num_sims):
        home_goals = np.random.poisson(self.home_xg, num_sims)
        return home_goals

    def simulate_away(self, num_sims):
        away_goals = np.random.poisson(self.away_xg, num_sims)
        return away_goals

    def simulate(self):
        return [self.simulate_home(), self.simulate_away()]

    def probabilities(self):
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        home = sum(poisson.pmf(k, mu_1) * poisson.cdf(k - 1, mu_2) for k in range(10))
        draw = sum(poisson.pmf(k, mu_1) * poisson.pmf(k, mu_2) for k in range(10))
        away = sum(poisson.pmf(k, mu_2) * poisson.cdf(k - 1, mu_1) for k in range(10))

        self.prob_home = home
        self.prob_draw = draw
        self.prob_away = away

        return [home, draw, away]

    def print_stats(self):
        string = (
            f"{self}\n"
            f"Home goals: {round(self.home_xg, 2)}\n"
            f"Away goals: {round(self.away_xg, 2)}\n"
            f"Prob home: {round(self.prob_home, 2)}\n"
            f"Prob draw: {round(self.prob_draw, 2)}\n"
            f"Prob away: {round(self.prob_away, 2)}\n")

        print(string)
        return string

    def __str__(self):
        return f"{self.home_team} - {self.away_team}"

Match('Turkey', 'Italy').print_stats()