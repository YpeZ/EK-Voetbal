from constants import groepen
from Match import Match
from Fixture import Fixture
import json
import pandas as pd


class Group:
    def __init__(self, key):
        self.teams = groepen[key]
        self.fixtures = self.get_fixtures()
        self.standings = self.simulate_standings()

    def get_fixtures(self):

        fixture_1 = Match(self.teams[0],
                          self.teams[1])
        fixture_2 = Match(self.teams[2],
                          self.teams[3])

        fixture_3 = Match(self.teams[0],
                          self.teams[2])
        fixture_4 = Match(self.teams[1],
                          self.teams[3])

        fixture_5 = Match(self.teams[0],
                          self.teams[3])
        fixture_6 = Match(self.teams[1],
                          self.teams[2])

        fixture_list = [fixture_1,
                        fixture_2,
                        fixture_3,
                        fixture_4,
                        fixture_5,
                        fixture_6]

        return fixture_list

    def simulate_standings(self, type='df'):

        standings = dict()
        for team in self.teams:
            standings.update({team: {'M': 0,
                                     'W': 0,
                                     'D': 0,
                                     'L': 0,
                                     'G': 0,
                                     'GA': 0,
                                     'PTS': 0}})

        for fixture in self.fixtures:
            h = fixture.home_team
            a = fixture.away_team

            # Simulate result of fixture
            sim = fixture.simulate()
            # Update standings
            standings[h]['M'] += 1
            standings[a]['M'] += 1
            standings[h]['W'] += int(sim[0] > sim[1])
            standings[a]['W'] += int(sim[1] > sim[0])
            standings[h]['D'] += int(sim[0] == sim[1])
            standings[a]['D'] += int(sim[1] == sim[0])
            standings[h]['L'] += int(sim[0] < sim[1])
            standings[a]['L'] += int(sim[1] < sim[0])
            standings[h]['G'] += sim[0]
            standings[h]['GA'] += sim[1]
            standings[a]['G'] += sim[1]
            standings[a]['GA'] += sim[0]
            standings[h]['PTS'] = 3 * standings[h]['W'] + standings[h]['D']
            standings[a]['PTS'] = 3 * standings[a]['W'] + standings[a]['D']

        if type == 'dict':
            return standings
        standings_df = pd.DataFrame.from_dict(standings, orient='index')
        standings_df.sort_values(by=['PTS', 'G'],
                                 ascending=[False, False], inplace=True)

        return standings_df

    def average_points(self, num_sims=1000, sort=False):
        total_table = {team: {'M': 0, 'W': 0, 'D': 0, 'L': 0, 'G': 0, 'GA': 0, 'PTS': 0}
                       for team in self.teams}

        for sim in range(num_sims):
            sim_standings = self.simulate_standings(type='dict')

            for team, values in sim_standings.items():
                for key, team_values in values.items():
                    total_table[team][key] += team_values

        for team, values in total_table.items():
            for key, team_values in values.items():
                total_table[team][key] /= num_sims

        if sort:
            total_table = dict(sorted(total_table.items(),
                                      key=lambda tup: tup[1]['PTS'],
                                      reverse=True))

        return total_table
