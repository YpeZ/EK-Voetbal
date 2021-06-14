#!/usr/bin/python3
import pandas as pd

from constants import groepen
from Match import Match
from Group import Group

for groep_idx, teams in groepen.items():
    groep = Group(groep_idx)
    print(f'Group {groep_idx}')
    for fixture in groep.fixtures[:]:
        fixture.print_stats()

# Second round
print("Second round")
Match('Croatia', 'Poland', True).print_stats()
Match('Portugal', 'Wales', True).print_stats()
Match('Italy', 'Ukraine', True).print_stats()
Match('Belgium', 'Slovakia', True).print_stats()
Match('Switzerland', 'Denmark', True).print_stats()
Match('Netherlands', 'Germany', True).print_stats()
Match('England', 'France', True).print_stats()
Match('Spain', 'Russia', True).print_stats()

# Quarter finals
print("Quarter finals")
Match('Croatia', 'Portugal', True).print_stats()
Match('Italy', 'Belgium', True).print_stats()
Match('Denmark', 'Germany', True).print_stats()
Match('France', 'Spain', True).print_stats()

# Semifinals
print("Semifinals")
Match('Portugal', 'Italy', True).print_stats()
Match('Denmark', 'Spain', True).print_stats()

# Final
print("Final")
Match('Italy', 'Denmark', True).print_stats()

for groep_idx, teams in groepen.items():
    groep = Group(groep_idx)
    print(f"Group {groep_idx}")
    group_table = groep.average_points(sort=True)
    print(pd.DataFrame.from_dict(group_table, orient='index'))
