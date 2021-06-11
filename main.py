from constants import groepen
from Match import Match
from Group import Group

for groep_idx, teams in groepen.items():
    groep = Group(groep_idx)
    print(f'Group {groep_idx}')
    for fixture in groep.fixtures[:]:
        print(fixture)
        print(f'Home goals: {round(fixture.home_xg, 2)}')
        print(f'Away goals: {round(fixture.away_xg, 2)}')
        print(f'Prob home: {round(fixture.prob_home, 2)}')
        print(f'Prob draw: {round(fixture.prob_draw, 2)}')
        print(f'Prob away: {round(fixture.prob_away, 2)}')
        print('\n')
