from constants import groepen
from Group import Group
from Match import Match


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
        self.round_of_16()


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
        :return: dictionary containing second round fixtures
        """
        group_lists = {group_idx: list(self.group_results[group_idx].keys())
                       for group_idx in self.group_results.keys()}

        matchups = [
            [group_lists['B'][0], self.third_place_ranked[list(self.third_place_ranked.keys())[0]]],
            [group_lists['A'][0], group_lists['C'][1]],
            [group_lists['F'][0], self.third_place_ranked[list(self.third_place_ranked.keys())[1]]],
            [group_lists['D'][1], group_lists['E'][1]],
            [group_lists['E'][0], self.third_place_ranked[list(self.third_place_ranked.keys())[2]]],
            [group_lists['D'][0], group_lists['F'][1]],
            [group_lists['C'][0], self.third_place_ranked[list(self.third_place_ranked.keys())[3]]],
            [group_lists['A'][1], group_lists['B'][1]]
        ]

        matches = [Match(matchup[0], matchup[1], extra_time=True) for matchup in matchups]
        ro_16_winners = [match.winner for match in matches]

        return ro_16_winners


tour = Tournament()
tour.round_of_16()
print(tour.third_places())

