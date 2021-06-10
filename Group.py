from constants import groepen
from Match import Match


class Group:
    def __init__(self, key):
        self.teams = groepen[key]

    def fixtures(self):
        fixture_1 = [self.teams[0],
                     self.teams[1]]
        fixture_2 = [self.teams[2],
                     self.teams[3]]

        fixture_3 = [self.teams[0],
                     self.teams[2]]
        fixture_4 = [self.teams[1],
                     self.teams[3]]

        fixture_5 = [self.teams[0],
                     self.teams[3]]
        fixture_6 = [self.teams[1],
                     self.teams[2]]

        fixture_list = [fixture_1,
                        fixture_2,
                        fixture_3,
                        fixture_4,
                        fixture_5,
                        fixture_6]

        return fixture_list

groep = Group('A')
print(groep.teams)
print(groep.fixtures())