from constants import groepen
from Group import Group
from Match import Match
from utils import get_third_place_order


class Tournament():
    """
    Class for simulating an entire tournament
    """

    def __init__(self):
        self.groups = {group_idx: Group(group_idx) for group_idx in groepen.keys()}
        self.group_results = {group_idx: self.groups[group_idx].standings for group_idx in self.groups.keys()}
        self.group_lists = {group_idx: list(self.group_results[group_idx].keys())
                            for group_idx in self.group_results.keys()}
        self.third_place_ranked = self.third_places()
        self.quarter_finalists = self.round_of_16()
        self.semi_finalists = self.quarter_finals()
        self.finalists = self.semi_finals()
        self.winner = self.final()

    def third_places(self):
        third_placed = {group_idx: self.group_lists[group_idx][2]
                        for group_idx in self.group_results}

        third_placed_points = {group_idx: {'country': third_placed[group_idx],
                                           'results': self.group_results[group_idx][third_placed[group_idx]]}
                               for group_idx in self.group_results}

        third_placed_points = dict(sorted(third_placed_points.items(), key=lambda tup: (tup[1]['results']['PTS'],
                                                                                        tup[1]['results']['GD'],
                                                                                        tup[1]['results']['G']),
                                          reverse=True))

        third_placed_ranked = {group_idx: third_placed_points[group_idx]['country']
                               for group_idx in third_placed_points.keys()}

        return third_placed_ranked

    def round_of_16(self):
        """
        Simulate the second round of the tournament based on the group stage results
        :return: list of round of sixteen winners
        """
        group_lists = {group_idx: list(self.group_results[group_idx].keys())
                       for group_idx in self.group_results.keys()}

        third_placed_list = get_third_place_order(self.third_place_ranked)

        matchups = [
            [group_lists['B'][0], third_placed_list[0]],
            [group_lists['A'][0], group_lists['C'][1]],
            [group_lists['F'][0], third_placed_list[3]],
            [group_lists['D'][1], group_lists['E'][1]],
            [group_lists['E'][0], third_placed_list[2]],
            [group_lists['D'][0], group_lists['F'][1]],
            [group_lists['C'][0], third_placed_list[1]],
            [group_lists['A'][1], group_lists['B'][1]]
        ]

        matches = [Match(matchup[0], matchup[1], extra_time=True) for matchup in matchups]
        ro_16_winners = [match.winner for match in matches]

        return ro_16_winners

    def quarter_finals(self):
        """
        Method to simulate quarter finals of the tournament based on results from
        the round of 16 fixtures
        :return: list of quarter finals winners
        """
        qf_matchups = [
            [self.quarter_finalists[0], self.quarter_finalists[1]],
            [self.quarter_finalists[2], self.quarter_finalists[3]],
            [self.quarter_finalists[4], self.quarter_finalists[5]],
            [self.quarter_finalists[6], self.quarter_finalists[7]]
        ]

        qf_matches = [Match(matchup[0], matchup[1], extra_time=True)
                      for matchup in qf_matchups]

        qf_winners = [match.winner for match in qf_matches]

        return qf_winners

    def semi_finals(self):
        """
        Method to simulate semi finals of the tournament based on results from
        the quarter finals fixtures
        :return: list of semi finals winners
        """
        sf_matchups = [
            [self.semi_finalists[0], self.semi_finalists[1]],
            [self.semi_finalists[2], self.semi_finalists[3]]
        ]

        sf_matches = [Match(matchup[0], matchup[1], extra_time=True)
                      for matchup in sf_matchups]

        sf_winners = [match.winner for match in sf_matches]

        return sf_winners

    def final(self):
        """
        Method to simulate the final of the tournament based on results from
        the semi finals fixtures
        :return: string of the name of final winner
        """

        final_match = Match(self.finalists[0], self.finalists[1], extra_time=True)

        return final_match.winner

tour = Tournament()