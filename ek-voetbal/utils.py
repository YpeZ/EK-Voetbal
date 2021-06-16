def get_third_place_order(group_dict: dict) -> list:
    """
    Collect the 'order' in which the best four third placed teams in the
    group stage play their round of 16.
    The 'first' team faces the winner of Group B, the 'second' team the
    winner of Group F, the 'third' team the winner of group E, and the
    'fourth' team the winner of Group C in the round of sixteen
    :param group_dict: a dictionary consisting of group name and third
    placed team, ordered by the team that scored the most points
    :return: list of teams in the above mentioned order
    """
    # Collect four groups with best number 3
    group_list = list(group_dict.keys())[:4]
    # Order this list by alphabet
    group_list = sorted(group_list)
    # Add the group names to form a code
    third_code = "".join(group_list)

    codes_to_order = {
        'ABCD': ['A', 'D', 'B', 'C'],
        'ABCE': ['A', 'E', 'B', 'C'],
        'ABCF': ['A', 'F', 'B', 'C'],
        'ABDE': ['D', 'E', 'A', 'B'],
        'ABDF': ['D', 'F', 'A', 'B'],
        'ABEF': ['E', 'F', 'B', 'A'],
        'ACDE': ['E', 'D', 'C', 'A'],
        'ACDF': ['F', 'D', 'C', 'A'],
        'ACEF': ['E', 'F', 'C', 'A'],
        'ADEF': ['E', 'F', 'D', 'A'],
        'BCDE': ['E', 'D', 'B', 'C'],
        'BCDF': ['F', 'D', 'C', 'B'],
        'BCEF': ['B', 'C', 'E', 'F'],
        'BDEF': ['F', 'E', 'D', 'B'],
        'CDEF': ['F', 'E', 'D', 'C']
    }

    new_group_list = codes_to_order[third_code]

    country_list = [group_dict[idx] for idx in new_group_list]

    return country_list