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

        self.penalties = [0, 0]
        self.result = self.simulate(num_sims=1)
        self.winner = [self.home_team, self.away_team][self.result.index(max(self.result))]

    def __str__(self):
        return f"{self.home_team} - {self.away_team}"

    def get_home_alpha(self) -> float:
        return alphabeta.loc[self.home_team, 'alpha']

    def get_home_beta(self) -> float:
        return alphabeta.loc[self.home_team, 'beta']

    def get_away_alpha(self) -> float:
        return alphabeta.loc[self.away_team, 'alpha']

    def get_away_beta(self) -> float:
        return alphabeta.loc[self.away_team, 'beta']

    def get_home_xg(self) -> float:
        home_xg = self.home_alpha * self.away_beta
        return home_xg

    def get_away_xg(self) -> float:
        away_xg = self.home_beta * self.away_alpha
        return away_xg

    def get_prob_home(self) -> float:
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        home = sum(poisson.pmf(k, mu_1) * poisson.cdf(k - 1, mu_2) for k in range(10))
        return home

    def get_prob_draw(self) -> float:
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        draw = sum(poisson.pmf(k, mu_1) * poisson.pmf(k, mu_2) for k in range(10))
        return draw

    def get_prob_away(self) -> float:
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        away = sum(poisson.pmf(k, mu_2) * poisson.cdf(k - 1, mu_1) for k in range(10))
        return away

    def simulate_home(self, num_sims=1, extra_time=False) -> int:
        mu_1 = self.home_xg
        if extra_time:
            mu_1 /= 3
        home_goals = np.random.poisson(mu_1, num_sims)
        if num_sims == 1:
            home_goals = int(home_goals)
        return home_goals

    def simulate_away(self, num_sims=1, extra_time=False) -> int:
        mu_2 = self.away_xg
        if extra_time:
            mu_2 /= 3
        away_goals = np.random.poisson(mu_2, num_sims)
        if num_sims == 1:
            away_goals = int(away_goals)
        return away_goals

    def simulate(self, num_sims=1) -> list:
        """
        Simulate the number of home and away goals scored in a match.
        If the score is equal and the match in in the knockout stage,
        first play an extra 30 minutes and if the score remains equal,
        do a penalty shootout
        :param num_sims: the number of times to simulate the match
        :return: a list containing the total number of home and away goals, respectively
        """
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
                home_penalties = (home == away) * penalties[self.home_team]
                away_penalties = (home == away) * penalties[self.away_team]

                home += home_penalties
                away += away_penalties

        return [home, away]

    def probabilities(self):
        """Compute the probabilities for home win, draw or away win and return as dict"""
        mu_1 = self.home_xg
        mu_2 = self.away_xg

        home = sum(poisson.pmf(k, mu_1) * poisson.cdf(k - 1, mu_2) for k in range(10))
        draw = sum(poisson.pmf(k, mu_1) * poisson.pmf(k, mu_2) for k in range(10))
        away = sum(poisson.pmf(k, mu_2) * poisson.cdf(k - 1, mu_1) for k in range(10))

        return {'home': home, 'draw': draw, 'away': away}

    def penalty_shootout(self, num_sims) -> dict:
        """
        Simulate a penalty shootout until there is a large enough difference
        to conclude a winner
        :param num_sims: number of shootouts to simulate
        :return: a dictionary containing for both teams the number of penalties scored
        """
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
            self.penalties = [home_pens, away_pens]

        result = {self.home_team: home_pens, self.away_team: away_pens}

        return result

    def print_stats(self):
        """Print the expected goals and win probabilities"""
        probs = self.probabilities()
        prob_home, prob_draw, prob_away = probs['home'], probs['draw'], probs['away']
        stats_string = (
            f"{self}\n"
            f"Home goals: {round(self.home_xg, 2)}\n"
            f"Away goals: {round(self.away_xg, 2)}\n"
            f"Prob home: {round(prob_home, 2)}\n"
            f"Prob draw: {round(prob_draw, 2)}\n"
            f"Prob away: {round(prob_away, 2)}\n")

        print(stats_string)

        return stats_string

    def print_result(self):
        """Print the result of the Match in the format
        'home_team - away_team: 2 - 3' or
        'home_team - away_team: 2 - 2 (4 - 3)' in case
        of a penalty shootout
        """
        if sum(self.penalties) == 0:
            result_string = (
                f"{self.home_team} - {self.away_team}: " 
                f"{' - '.join([str(res) for res in self.result])}"
            )
        else:
            home_result = self.result[0] - self.penalties[0]
            away_result = self.result[1] - self.penalties[1]
            home_pens, away_pens = self.penalties[0], self.penalties[1]

            result_string = (
                f"{self.home_team} - {self.away_team}: " 
                f"{home_result} - {away_result} ({home_pens} - {away_pens})"
            )

        print(result_string)