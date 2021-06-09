import numpy as np
import pandas as pd
import json

from datetime import datetime


def prepare_data(match_data: pd.DataFrame) -> dict:
    """
    Transform the DataFrame of all matches to a dictionary of matches per country
    :param match_data: a pandas DataFrame object consisting of all match data
    :return: dictionary of matches for each country
    """

    # Collect the names of all countries in the dataset in all_countries
    all_countries: list = set(match_data['home_team'])
    # Create a dictionary to collect all match data for each country
    matches_dict = dict()
    # Loop through all countries and add their data to the matches_dict
    for country in all_countries:
        matches_list = list()

        home_matches = match_data[match_data['home_team'] == country].copy()
        home_matches = home_matches[['date', 'away_team', 'home_score', 'away_score', 'tournament', 'neutral']]
        home_matches.rename(columns={'away_team': 'opponent', 'home_score': 'G', 'away_score': 'GA'}, inplace=True)
        matches_list.extend(home_matches.to_dict('records'))

        away_matches = match_data[match_data['away_team'] == country].copy()
        away_matches = away_matches[['date', 'home_team', 'away_score', 'home_score', 'tournament', 'neutral']]
        away_matches.rename(columns={'home_team': 'opponent', 'away_score': 'G', 'home_score': 'GA'}, inplace=True)
        matches_list.extend(away_matches.to_dict('records'))

        matches_list = sorted(matches_list, key=lambda item: item['date'])
        matches_dict.update({country: matches_list})

        with open('clean_match_data.json', 'w') as f:
            json.dump(matches_dict, f, ensure_ascii=False, indent=4)

    return matches_dict


def initialize_alphabetas(clean_data: dict) -> dict:
    """
    Create the initial alphabeta dataset using the cleaned dataset
    :param clean_data: the prepared dataset in dict
    :return: dictionary containing alpha and beta for each country in the cleaned dataset
    """
    num_games = sum(len(matches) for country, matches in clean_data.items())
    G_sum = 0
    for country in clean_data.keys():
        G_sum += sum(game['G'] for game in clean_data[country])

    G_ave = G_sum / num_games

    alphabet_dict = dict()
    for country, games in clean_data.items():
        alpha = ((sum(game['G'] for game in games) / len(games)) / G_ave)
        beta = (sum(game['GA'] for game in games) / len(games)) / G_ave
        # beta = (sum(game['GA'] for game in games)) / len(games)) / G_ave

        alphabet_dict.update({country: {'alpha': alpha, 'beta': beta}})

    return alphabet_dict


def calculate_alphabetas(force_new: bool = False):
    """
    Calculate the alpha and beta values for each country in the dataset.
    Including countries that do not participate in the 2020 European Championship
    :param force_new: specifies whether to generate a new dictionary or open one from file
    :return: pandas DataFrame
    """

    match_data = pd.read_csv('data/match_results.csv')
    match_data = match_data[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'neutral']]

    if force_new:
        # Open the cleaned data dictionary by running the prepare data function
        clean_data: dict = prepare_data(match_data)
    else:
        # Open the cleaned data dictionary from file
        with open('data/clean_match_data.json', 'r') as f:
            clean_data = json.load(f)

    alphabet_dict = initialize_alphabetas(clean_data)

    ## Update alphas
    att_d_rate = 0.009
    today = datetime.today()
    country_names = [country for country in clean_data.keys()]
    for country, games in clean_data.items():
        alpha_sum, beta_sum, goals_sum = 0, 0, 0

        for game in games:
            opponent = game['opponent']
            if opponent not in country_names:
                continue
            G_ij = game['G']

            game_date = datetime.strptime(game['date'], '%Y-%m-%d')
            days_ago = abs(today - game_date).days

            d_factor = np.exp(-days_ago * att_d_rate)

            goals_sum += G_ij * d_factor
            beta_sum += alphabet_dict[opponent]['beta'] * d_factor

        # alphabet_df.update({country: })
        alphabet_dict[country]['alpha'] = goals_sum / beta_sum

    # Convert the dictionary to a pandas DataFrame and save it as csv
    alphabet_df = pd.DataFrame.from_dict(alphabet_dict, orient='index')
    alphabet_df.sort_values(by='alpha', ascending=False, inplace=True)

    alphabet_df.to_csv('output/alphabet.csv')

    return alphabet_df


if __name__ == '__main__':
    calculate_alphabetas()
