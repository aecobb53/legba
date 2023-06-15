# import sys
# import os
import json
import requests

# classes_path = os.path.join(os.path.abspath('.'), 'calsses')
# sys.path.append(classes_path)


# x=1
details = [
    'date': datetime(2023, 6, 1), 'work': 6.5, 'meeting': 1.5, 'other': 0,
    'date': datetime(2023, 6, 2), 'work': 6, 'meeting': 0.5, 'other': 0,
    'date': datetime(2023, 6, 5), 'work': 6, 'meeting': 2, 'other': 0,
    'date': datetime(2023, 6, 6), 'work': 6.5, 'meeting': 0.5, 'other': 0,
    'date': datetime(2023, 6, 7), 'work': 5.5, 'meeting': 1, 'other': 0,
    'date': datetime(2023, 6, 8), 'work': 5.5, 'meeting': 1.5, 'other': 0,
    'date': datetime(2023, 6, 9), 'work': 6, 'meeting': 0.5, 'other': 0,
    'date': datetime(2023, 6, 12), 'work': 7.5, 'meeting': 0.5, 'other': 0,
    'date': datetime(2023, 6, 13), 'work': 5.5, 'meeting': 1, 'other': 0,
    'date': datetime(2023, 6, 14), 'work': 5.5, 'meeting': 1, 'other': 0,
    'date': datetime(2023, 6, 15), 'work': 00000, 'meeting': 1.5, 'other': 0,
]


