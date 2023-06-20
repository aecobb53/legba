# import sys
# import os
import json
import re
import requests
from datetime import datetime, timedelta

# classes_path = os.path.join(os.path.abspath('.'), 'calsses')
# sys.path.append(classes_path)
# response = requests.get('http://hamster.nax.lol:8201/timecard')

def reset_database():
    # response = requests.get('http://hamster.nax.lol:8201/timecard')
    payload = {'records': []}
    response = requests.post('http://hamster.nax.lol:8201/timecard-set', json=payload)
    a = response.json()
    x=1
x=1
reset_database()

# # x=1
# details = [
#     {'date': datetime(2023, 6, 1), 'work': 6.5, 'meeting': 1.5, 'other': 0},
#     {'date': datetime(2023, 6, 2), 'work': 6, 'meeting': 0.5, 'other': 0},

#     {'date': datetime(2023, 6, 5), 'work': 6, 'meeting': 2, 'other': 0},
#     {'date': datetime(2023, 6, 6), 'work': 6.5, 'meeting': 0.5, 'other': 0},
#     {'date': datetime(2023, 6, 7), 'work': 5.5, 'meeting': 1, 'other': 0},
#     {'date': datetime(2023, 6, 8), 'work': 5.5, 'meeting': 1.5, 'other': 0},
#     {'date': datetime(2023, 6, 9), 'work': 6, 'meeting': 0.5, 'other': 0},

#     {'date': datetime(2023, 6, 12), 'work': 7.5, 'meeting': 0.5, 'other': 0},
#     {'date': datetime(2023, 6, 13), 'work': 5.5, 'meeting': 1, 'other': 0},
#     {'date': datetime(2023, 6, 14), 'work': 5.5, 'meeting': 1, 'other': 0},
#     {'date': datetime(2023, 6, 15), 'work': 00000, 'meeting': 1.5, 'other': 0},
# ]

# for item in details:
#     x=1
#     payload = {
        
#     }





# details = {
#     datetime.strftime(datetime(2023, 6, 1), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 8, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 1.5, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 2), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 7, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 0.5, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 5), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 8, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 2, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 6), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 7, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 0.5, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 7), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 6.5, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 1, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 8), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 7, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 1.5, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 9), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '', 'endtime': '', 'duration': 3.5, 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 0.5, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 12), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': 9, 'endtime': '15:30', 'duration': '', 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 0.5, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 13), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': 9, 'endtime': '15:30', 'duration': '', 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 1, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 14), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': 9, 'endtime': '15:30', 'duration': '', 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 1, 'shorthand': 'meetings'},
#         ],
#     },
#     datetime.strftime(datetime(2023, 6, 15), "%Y-%m-%d"): {
#         'entries': [
#             {'starttime': '7:30', 'endtime': '', 'duration': '', 'shorthand': 'workday'},
#             {'starttime': '', 'endtime': '', 'duration': 2.5, 'shorthand': 'meetings'},
#         ],
#     },
# }

# new_details = {}
# for dt, item in details.items():
#     x=1
#     entries = []
#     for ent in item['entries']:
#         if ent['starttime'] != '':
#             entries.append({'starttime': str(ent['starttime']), 'shorthand': ent['shorthand']})
#         if ent['endtime'] != '':
#             entries.append({'endtime': str(ent['endtime']), 'shorthand': ent['shorthand']})
#         if ent['duration'] != '':
#             entries.append({'duration': float(ent['duration']), 'shorthand': ent['shorthand']})
#     new_details[dt] = {
#         'entries': entries
#     }
# with open('data/timecard/dev_timesheet_for_use_and_testing.json', 'w') as jf:
#     jf.write(json.dumps(new_details, indent=4))

with open('data/timecard/dev_timesheet_for_use_and_testing.json', 'r') as jf:
    data = json.load(jf)

for date, record in data.items():
    x=1
    for entry in record['entries']:
        url = f"http://hamster.nax.lol:8201/timecard-entry"
        body = {
            'shorthand': entry['shorthand'],
            'day': date,
        }
        if 'starttime' in entry:
            body['start_time'] = f"{date}T{entry['starttime']}"
        if 'endtime' in entry:
            body['end_time'] = f"{date}T{entry['endtime']}"
        if 'duration' in entry:
            body['duration'] = float(entry['duration'])
        response = requests.post(
            url,
            json=body
        )
        a = response.json()
        x=1

x=1
response = requests.get('http://hamster.nax.lol:8201/timecard')
resp = response.json()
with open('data/validation_file.json', 'w') as jf:
    jf.write(json.dumps(resp, indent=4))
x=1


