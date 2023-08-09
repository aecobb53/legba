# import sys
# import os
import json
import re
import requests
from datetime import datetime, timedelta

def reset_database():
    payload = {'records': []}
    response = requests.post('http://hamster.nax.lol:8201/timecard-set', json=payload)
    return response.json()

def post_data(url_base, path):
    with open(path, 'r') as jf:
        data = json.load(jf)

    for date, record in data.items():
        for entry in record['entries']:
            url = f"{url_base}/timecard-entry"
            body = {
                'shorthand': entry['shorthand'],
                'day': date,
            }
            if 'start_time' in entry:
                body['start_time'] = f"{date}T{entry['start_time']}"
            if 'end_time' in entry:
                body['end_time'] = f"{date}T{entry['end_time']}"
            if 'duration' in entry:
                body['duration'] = float(entry['duration'])
            response = requests.post(
                url,
                json=body
            )
            if response.status_code != 200:
                x=1


def get_charge_code_data(url_base, save_file=True):
    response = requests.get(f'{url_base}/timecard')
    resp = response.json()
    if save_file:
        with open('data/validation_file.json', 'w') as jf:
            jf.write(json.dumps(resp, indent=4))
    return resp

x=1

# response = requests.post(
#     'http://hamster.nax.lol:8201/timecard-entry',
#     headers={'Content-type': 'application/json', 'Accept': 'text/plain'},
#     data=json.dumps({
#         # 'start_time': '08:00:00',
#         # 'end_time': '08:00:00',
#         'duration': '08',
#         # 'shorthand': 'fto',
#         'day': '2023-08-04',
#     })
# )
# try:
#     resp = response.json()
# except:
#     pass
x=1

if True:
    reset_database()
    post_data(url_base='http://hamster.nax.lol:8201', path='data/timecard/dev_timesheet_for_use_and_testing.json')
    resp = get_charge_code_data(url_base='http://hamster.nax.lol:8201')
    x=1
else:
    resp = get_charge_code_data(url_base='http://hamster.nax.lol:8201')
    x=1


x=1

