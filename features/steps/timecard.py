import requests
import json
from behave import given, when, then
# from classes.timecard import (
#     TimecardEntry,
#     DayOfEntries,
#     Timecard,
# )

local_url = 'http://0.0.0.0:8201'


@given('I start with an empty database')
def empty_database(context):
    payload = {'records': []}
    response = requests.post(f'{local_url}/timecard-set', json=payload)
    assert response.status_code == 200
    assert response.json() == {'records': []}

@when('I post a timecard entry')
def post_a_timecard(context):
    payload = {'shorthand': 'working', 'day': '2023-06-01', 'duration': 8.0}
    response = requests.post(f'{local_url}/timecard-entry', json=payload)
    assert response.status_code == 200
    # assert response.json()["update_datetime"] ==  "20230705T040013.946114Z"
    # assert response.json()["changelog"] ==  []
    # assert response.json()["charge_code"] ==  None
    # assert response.json()["shorthand"] ==  "working"
    # assert response.json()["note"] ==  None
    # assert response.json()["description"] ==  None
    # assert response.json()["start_time"] ==  None
    # assert response.json()["end_time"] ==  None
    # assert response.json()["duration"] ==  "8:0:0"
    # assert response.json()["day"] ==  "20230601Z"

@when('I post June timecard entries')
def post_june_timecard(context):
    with open('/home/acobb/git/legba/data/timecard/dev_timesheet_for_use_and_testing.json', 'r') as jf:
        data = json.load(jf)
    for date, record in data.items():
        for entry in record['entries']:
            url = f"{local_url}/timecard-entry"
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
                print('')
                print(date)
                print(json.dumps(body,  indent=4))
                print(f"status_code: {response.status_code}")
                print(f"json: {response.json()}")
            assert response.status_code == 200

@then('I can get all data back')
def validate_timecard_data(context):
    response = requests.get(f'{local_url}/timecard')
    assert response.status_code == 200
    assert response.json() == {
        "20230601Z": {
            "CHARGE.CODE.WORK": 8.0
        }
    }

@then('I can get June charge code data')
def validate_timecard_data(context):
    params = {
        'day': '2023-06',
    }
    response = requests.get(f'{local_url}/timecard', params=params)
    assert response.status_code == 200
    print('')
    print('')
    print('')
    print(json.dumps(response.json(), indent=4))
    assert response.json() == {
          "20230601Z": {
              "CHARGE.CODE.WORK": 8.0,
              "CHARGE.CODE.MEETING": 1.5
          },
          "20230602Z": {
              "CHARGE.CODE.WORK": 7.0,
              "CHARGE.CODE.MEETING": 0.5
          },
          "20230605Z": {
              "CHARGE.CODE.WORK": 8.0,
              "CHARGE.CODE.MEETING": 2.0
          },
          "20230606Z": {
              "CHARGE.CODE.WORK": 7.0,
              "CHARGE.CODE.MEETING": 0.5
          },
          "20230607Z": {
              "CHARGE.CODE.WORK": 6.5,
              "CHARGE.CODE.MEETING": 1.0
          },
          "20230608Z": {
              "CHARGE.CODE.WORK": 7.0,
              "CHARGE.CODE.MEETING": 1.5
          },
          "20230609Z": {
              "CHARGE.CODE.WORK": 3.5,
              "CHARGE.CODE.MEETING": 0.5
          },
          "20230612Z": {
              "CHARGE.CODE.MEETING": 0.5,
              "CHARGE.CODE.WORK": 6.5
          },
          "20230613Z": {
              "CHARGE.CODE.MEETING": 1.0,
              "CHARGE.CODE.WORK": 6.5
          },
          "20230614Z": {
              "CHARGE.CODE.MEETING": 1.0,
              "CHARGE.CODE.WORK": 6.5
          },
          "20230615Z": {
              "CHARGE.CODE.MEETING": 2.5,
              "CHARGE.CODE.WORK": 8.5
          },
          "20230616Z": {
              "CHARGE.CODE.MEETING": 0.5,
              "CHARGE.CODE.WORK": 39.0
          },
          "20230617Z": {
              "CHARGE.CODE.WORK": 1.0
          },
          "20230620Z": {
              "CHARGE.CODE.MEETING": 1.5,
              "CHARGE.CODE.WORK": 6.5
          },
          "20230621Z": {
              "CHARGE.CODE.MEETING": 0.5,
              "CHARGE.CODE.WORK": 33.0
          },
          "20230622Z": {
              "CHARGE.CODE.MEETING": 1.5,
              "CHARGE.CODE.WORK": 5.5
          },
          "20230623Z": {
              "CHARGE.CODE.MEETING": 1.0,
              "CHARGE.CODE.WORK": 8.0
          },
          "20230626Z": {
              "CHARGE.CODE.MEETING": 0.5,
              "CHARGE.CODE.WORK": 7.75
          },
          "20230627Z": {
              "CHARGE.CODE.MEETING": 1.0,
              "CHARGE.CODE.WORK": 7.0
          },
          "20230628Z": {
              "CHARGE.CODE.MEETING": 6.0,
              "CHARGE.CODE.WORK": 2.0
          },
          "20230629Z": {
              "CHARGE.CODE.MEETING": 6.0,
              "CHARGE.CODE.WORK": 1.0
          },
          "20230630Z": {
              "CHARGE.CODE.FTO": 8.0
          }
      }
