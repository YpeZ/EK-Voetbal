from constants_values import groepen, group_matches
from Match import Match
import json
import pandas as pd


class Group:
    def __init__(self, key):
        self.key = key
        self.teams = groepen[key]
        self.fixtures = self.get_fixtures()
        self.standings = self.simulate_standings()
        # self.standings = self.sort_standings()
        self.ranking = self.rank_teams()

    def get_fixtures(self):

        fixture_matchups = [matchup for matchup in group_matches[self.key]]
        fixture_list = [Match(matchup[0], matchup[1]) for matchup in fixture_matchups]

        return fixture_list

    def simulate_standings(self, type='dict'):

        standings = dict()
        for team in self.teams:
            standings.update({team: {'M': 0,
                                     'W': 0,
                                     'D': 0,
                                     'L': 0,
                                     'G': 0,
                                     'GA': 0,
                                     'GD': 0,
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
            standings[h]['GD'] += sim[0] - sim[1]
            standings[a]['G'] += sim[1]
            standings[a]['GA'] += sim[0]
            standings[a]['GD'] += sim[1] - sim[0]
            standings[h]['PTS'] = 3 * standings[h]['W'] + standings[h]['D']
            standings[a]['PTS'] = 3 * standings[a]['W'] + standings[a]['D']

        standings = dict(sorted(standings.items(), key=lambda k: (k[1]['PTS'], k[1]['GD']),
                                reverse=True))

        if type == 'dict':
            return standings

        standings_df = pd.DataFrame.from_dict(standings, orient='index')
        standings_df.sort_values(by=['PTS', 'GD', 'G'],
                                 ascending=[False] * 3, inplace=True)

        return standings_df

    def sort_standings(self):
        points = [values['PTS'] for team, values in self.standings.items()]
        if len(set(points)) == 4:
            return self.standings

        if len(set(points)) == 1:
            goal_diffs = [values['GD'] for team, values in self.standings.items()]
            goals = [values['G'] for team, values in self.standings.items()]
            print(f"All equal points: {points}. GD: {goal_diffs}. Goals: {goals}")

        elif len(set(points)) == 2:
            if points.count(list(set(points))[0]) == 2:
                print(f"Two ties: {points}")
            else:
                print(f"Three-way tie: {points}")
        return self.standings

    def average_points(self, num_sims=1000, sort=True):
        total_table = {team: {'M': 0, 'W': 0, 'D': 0, 'L': 0, 'G': 0, 'GA': 0, 'GD': 0, 'PTS': 0}
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

    def rank_teams(self) -> list:
        """
        Create a list of teams ranked by their standings in the self.standings attribute
        :return: list of team names
        """
        ranked_teams = list(self.standings)

        return ranked_teams

    def print_results(self):
        for match in self.fixtures:
            match.print_result()
