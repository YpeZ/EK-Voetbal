# De verdeling van deelnemende landen over groepen
groepen = {
    'A': ['Turkey', 'Italy', 'Wales', 'Switzerland'],
    'B': ['Denmark', 'Finland', 'Belgium', 'Russia'],
    'C': ['Austria', 'North Macedonia', 'Netherlands', 'Ukraine'],
    'D': ['England', 'Croatia', 'Scotland', 'Czech Republic'],
    'E': ['Poland', 'Slovakia', 'Spain', 'Sweden'],
    'F': ['Hungary', 'Portugal', 'France', 'Germany']
}

group_matches = {
    'A': [
        ['Turkey', 'Italy'],
        ['Wales', 'Switzerland'],
        ['Turkey', 'Wales'],
        ['Italy', 'Switzerland'],
        ['Switzerland', 'Turkey'],
        ['Italy', 'Wales']
    ],
    'B': [
        ['Denmark', 'Finland'],
        ['Belgium', 'Russia'],
        ['Finland', 'Russia'],
        ['Denmark', 'Belgium'],
        ['Russia', 'Denmark'],
        ['Finland', 'Belgium']
    ],
    'C': [
        ['Austria', 'North Macedonia'],
        ['Netherlands', 'Austria'],
        ['Ukraine', 'North Macedonia'],
        ['Netherlands', 'Austria'],
        ['North Macedonia', 'Netherlands'],
        ['Ukraine', 'Austria']
    ],
    'D': [
        ['England', 'Croatia'],
        ['Scotland', 'Czech Republic'],
        ['Croatia', 'Czech Republic'],
        ['England', 'Scotland'],
        ['Croatia', 'Scotland'],
        ['Czech Republic', 'England']
    ],
    'E': [
        ['Poland', 'Slovakia'],
        ['Spain', 'Sweden'],
        ['Sweden', 'Slovakia'],
        ['Spain', 'Poland'],
        ['Slovakia', 'Spain'],
        ['Sweden', 'Poland']
    ],
    'F': [
        ['Hungary', 'Portugal'],
        ['France', 'Germany'],
        ['Hungary', 'France'],
        ['Portugal', 'Germany'],
        ['Portugal', 'France'],
        ['Germany', 'Hungary']
    ]
}