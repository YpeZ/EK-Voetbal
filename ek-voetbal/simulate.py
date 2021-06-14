from constants import groepen
import pandas as pd
from compute_alphabetas import calculate_alphabetas

# alphabet = calculate_alphabetas(no_friendly=True)
alphabet = pd.read_csv('../output/alphabet.csv', index_col=[0])
alphabet = alphabet.to_dict(orient='index')

for group, teams in groepen.items():
    teams = list(teams)
    print(f"\nGroup {group}: ")
    wedstrijd_1 = [alphabet[teams[0]]['alpha'] * alphabet[teams[1]]['beta'],
                   alphabet[teams[0]]['beta'] * alphabet[teams[1]]['alpha']]
    wedstrijd_2 = [alphabet[teams[2]]['alpha'] * alphabet[teams[3]]['beta'],
                   alphabet[teams[2]]['beta'] * alphabet[teams[3]]['alpha']]

    print(f"Wedstrijd 1: {teams[0]} - {teams[1]}: {round(wedstrijd_1[0], 2)} - {round(wedstrijd_1[1], 2)}")
    print(f"Wedstrijd 2: {teams[2]} - {teams[3]}: {round(wedstrijd_2[0], 2)} - {round(wedstrijd_2[1], 2)}")