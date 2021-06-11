from constants import groepen
from Match import Match
from Fixture import Fixture


class Group:
    def __init__(self, key):
        self.teams = groepen[key]
        self.fixtures = self.get_fixtures()

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