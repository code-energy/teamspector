_dataset = 'imdbws'
experiments = [
    {'id': 0,
     'dataset': _dataset,
     'team': ['producer', 'director'],
     'year_start': 1990,
     'year_end': 1991,
     'metrics': ['previous_ypct'],
     'filter': {'is_subject': True}},
    {'id': 1,
     'dataset': _dataset,
     'team': ['producer', 'director', 'writer'],
     'year_start': 1990,
     'year_end': 2012,
     'filter': {'is_subject': True}},
]
experiments = dict([(x['id'], x) for x in experiments])
