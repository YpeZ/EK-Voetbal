#!/usr/bin/python3
from Match import Match
from Group import Group
from constants_values import groepen
from scipy.stats import poisson
import numpy as np

granjero_ro16 = [
    Match('Croatia', 'Sweden'),
    Match('Portugal', 'Wales'),
    Match('Italy', 'Ukraine'),
    Match('Belgium', 'Germany'),
    Match('Switzerland', 'Denmark'),
    Match('Netherlands', 'Czech Republic'),
    Match('England', 'France'),
    Match('Spain', 'Austria')
]

granjero_qf = [
    Match('Sweden', 'Portugal'),
    Match('Italy', 'Belgium'),
    Match('Denmark', 'Netherlands'),
    Match('England', 'Spain')
]

granjero_sf = [
    Match('Portugal', 'Belgium'),
    Match('Denmark', 'Spain')
]

granjero_final = [
    Match('Belgium', 'Spain')
]


def match_pred(match: Match, game: str, all_points: bool):
    """

    :param match:
    :param game:
    :param all_points:
    :return:
    """
    home_xg = match.home_xg
    away_xg = match.away_xg

    probs = match.probabilities()
    prob_home, prob_draw, prob_away = probs['home'], probs['draw'], probs['away']

    home_g_dist = [poisson.pmf(goals, home_xg) for goals in range(10)]
    away_g_dist = [poisson.pmf(goals, away_xg) for goals in range(10)]

    points = np.array([[0.0] * 5] * 5)

    if game == 'knvb':
        for m in range(5):
            points[m][m] = 10 * prob_draw
            for n in range(m):
                points[m][n] += 10 * prob_home
                points[n][m] += 10 * prob_away
            for n in range(5):
                points[m][n] += 5 * home_g_dist[m] * away_g_dist[n]

    if game == 'uefa':
        for m in range(5):
            points[m][m] = 3 * prob_draw
            for n in range(m):
                points[m][n] += 3 * prob_home
                points[n][m] += 3 * prob_away
            for n in range(5):
                points[m][n] += 1 * home_g_dist[m] + 1 * away_g_dist[n]

    elif game == 'probability':
        for m in range(5):
            points[m][m] = 0 * prob_draw
            for n in range(m):
                points[m][n] += 0 * prob_home
                points[n][m] += 0 * prob_away
            for n in range(5):
                points[m][n] = round(1 * home_g_dist[m] * away_g_dist[n], 3)

    elif game == 'granjero':
        for m in range(5):
            points[m][m] = 1 * prob_draw
            for n in range(m):
                points[m][n] += 1 * prob_home
                points[n][m] += 1 * prob_away
            for n in range(5):
                points[m][n] += 1 * home_g_dist[m] \
                                + 1 * away_g_dist[n]
    elif game == 'excel_2':
        for m in range(5):
            points[m][m] = 20 * prob_draw + (10 * home_g_dist[m] + 10 * away_g_dist[m]) * prob_draw
            for n in range(m):
                points[m][n] = 20 * prob_home + (10 * home_g_dist[m] + 10 * away_g_dist[n]) * prob_home
                points[n][m] = 20 * prob_away + (10 * home_g_dist[m] + 10 * away_g_dist[n]) * prob_away

    else:
        for m in range(5):
            points[m][m] = 20 * prob_draw + (10 * home_g_dist[m] + 10 * away_g_dist[m]) * prob_draw
            for n in range(m):
                points[m][n] += 20 * prob_home + (10 * home_g_dist[m] + 10 * away_g_dist[n]) * prob_home
                points[n][m] += 20 * prob_away + (10 * home_g_dist[m] + 10 * away_g_dist[n]) * prob_away
            for n in range(5):
                points[m][n] += 10 * home_g_dist[m] + 10 * away_g_dist[n]

    max_score_idx = np.unravel_index(np.argmax(points, axis=None), points.shape)
    max_score_idx = [str(idx) for idx in max_score_idx]

    print(f"{match}: {' - '.join(max_score_idx)}")
    if all_points:
        print(points)


def optimize_pools(game: str, all_points: bool = False) -> None:
    for group_idx in list(groepen.keys()):
        group = Group(group_idx)
        print(f"Group {group_idx}")
        match_list = group.fixtures
        for match in match_list:
            match_pred(match, game, all_points)

    if game == 'granjero':
        print("\nRound of 16")
        match_list = granjero_ro16
        for match in match_list:
            match_pred(match, game, all_points)

        print("\nQuarter final")
        match_list = granjero_qf
        for match in match_list:
            match_pred(match, game, all_points)

        print("\nSemi final")
        match_list = granjero_sf
        for match in match_list:
            match_pred(match, game, all_points)

        print("\nFinal")
        match_list = granjero_final
        for match in match_list:
            match_pred(match, game, all_points)


if __name__ == '__main__':
    optimize_pools('knvb')
