import pandas as pd
import numpy as np
from scipy.stats import poisson
import os.path


file_path = os.path.dirname(__file__)
alphabeta = pd.read_csv(f'{file_path}/../output/alphabet.csv', index_col=[0])


class Match:
    def __init__(self, home_team, away_team, knockout=False):
        self.home_team = home_team
        self.away_team = away_team
        self.knockout = knockout

        self.home_alpha = self.get_home_alpha()
        self.home_beta = self.get_home_beta()
        self.away_alpha = self.get_away_alpha()
        self.away_beta = self.get_away_beta()

        self.home_xg = self.get_home_xg()
        self.away_xg = self.get_away_xg()

        self.result = self.simulate(num_sims=1)
        self.winner = [self.home_team, self.away_team][self.result.index(max(self.result))]

    def __str__(self):
        return f"{self.home_team} - {self.away_team}"

    def get_home_alpha(self):
        return alphabeta.loc[self.home_team, 'alpha']

    def get_home_beta(self):
        return alphabeta.loc[self.home_team, 'beta']

    def get_away_alpha(self):
        return alphabeta.loc[self.away_team, 'alpha']

    def get_away_beta(self):
        return alphabeta.loc[self.away_team, 'beta']

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

    def simulate_home(self, num_sims=1, extra_time=False):
        mu_1 = self.home_xg
        if extra_time:
            mu_1 /= 3
        home_goals = np.random.poisson(mu_1, num_sims)
        if num_sims == 1:
            home_goals = int(home_goals)
        return home_goals

    def simulate_away(self, num_sims=1, extra_time=False):
        mu_2 = self.away_xg
        if extra_time:
            mu_2 /= 3
        away_goals = np.random.poisson(mu_2, num_sims)
        if num_sims == 1:
            away_goals = int(away_goals)
        return away_goals

    def simulate(self, num_sims=1):
        home = self.simulate_home(num_sims)
        away = self.simulate_away(num_sims)

        if self.knockout:
            # Simulate 30 minutes of a match for knockout matches that end equal
            # after 90 minutes
            home_extra = (home == away) * self.simulate_home(num_sims, extra_time=True)
            away_extra = (home == away) * self.simulate_away(num_sims, extra_time=True)

            home += home_extra
            away += away_extra

            # If after extra time the scores are still level, a penalty shootout
            # will decide the winner
            if num_sims > 1 or home == away:
                penalties = self.penalty_shootout(num_sims)
                home_penalties = penalties[self.home_team]
                away_penalties = penalties[self.away_team]

                home, away = home + (home == away) * home_penalties, \
                             away + (home == away) * away_penalties

        return [home, away]

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
        stats_string = (
            f"{self}\n"
            f"Home goals: {round(self.home_xg, 2)}\n"
            f"Away goals: {round(self.away_xg, 2)}\n"
            f"Prob home: {round(self.prob_home, 2)}\n"
            f"Prob draw: {round(self.prob_draw, 2)}\n"
            f"Prob away: {round(self.prob_away, 2)}\n")

        print(stats_string)
        return stats_string

    def print_result(self):
        result_string = (
            f"{self.home_team} - {self.away_team}: {' - '.join([str(res) for res in self.result])}"
        )

        print(result_string)

    def penalty_shootout(self, num_sims) -> dict:
        home_pens = np.zeros(num_sims)
        away_pens = np.zeros(num_sims)

        for sim in range(num_sims):
            penalty_nr = 0
            pens_diff = 0

            # Simulate the first five penalties until there is a large enough
            # difference between the number scored
            while penalty_nr + pens_diff <= 5 and penalty_nr < 5:
                home_pens[sim] += np.random.binomial(p=0.75, n=1)
                away_pens[sim] += np.random.binomial(p=0.75, n=1)

                pens_diff = abs(home_pens[sim] - away_pens[sim])
                penalty_nr += 1

            # Simulate round by round if the number of penalties scored
            # is level after five penalty kicks
            while pens_diff == 0:
                home_pens[sim] += np.random.binomial(p=0.75, n=1)
                away_pens[sim] += np.random.binomial(p=0.75, n=1)

                pens_diff = abs(home_pens[sim] - away_pens[sim])
                penalty_nr += 1

        if num_sims == 1:
            home_pens, away_pens = int(home_pens), int(away_pens)

        result = {self.home_team: home_pens, self.away_team: away_pens}
        return result
