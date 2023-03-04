import json
from sqlite3 import paramstyle
from webbrowser import get
import requests

"""
https://github.com/dword4/nhlapi
"""
def get_stuff(url, params=None):
    resposne = requests.get(
        url=url,
        params=params
    )
    code = resposne.status_code
    data = resposne.json()
    return code, data

# url = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/calendar'

# # resposne = requests.get(url)
# # code = resposne.status_code
# # data = resposne.json()
# code, data = get_stuff(url)
# x=1

# url = data['items'][0]['$ref']
# x=1

# # resposne = requests.get(url)
# # code = resposne.status_code
# # data = resposne.json()
# code, data = get_stuff(url)
# # print(json.dumps(data, indent=2))



# # teams
# code, data = get_stuff('https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams')
# # print(json.dumps(data, indent=2))
# with open('deleteme.json', 'w') as tf:
#     tf.write(json.dumps(data, indent=4))

# # teams
# url = 'https://statsapi.web.nhl.com/api/v1/teams'
# code, data = get_stuff(url)
# # print(json.dumps(data, indent=2))
# with open('deleteme.json', 'w') as tf:
#     tf.write(json.dumps(data, indent=4))


# # Avs
# url = 'https://statsapi.web.nhl.com/api/v1/teams/21/stats'
# code, data = get_stuff(url)
# # print(json.dumps(data, indent=2))
# with open('deleteme.json', 'w') as tf:
#     tf.write(json.dumps(data, indent=4))


# Schedule
url = 'https://statsapi.web.nhl.com/api/v1/schedule'
params = {
    'teamId': 21,
    'startDate': '2023-01-01',
    'endDate': '2024-01-01'
}
code, data = get_stuff(url=url, params=params)
# print(json.dumps(data, indent=2))
with open('deleteme.json', 'w') as tf:
    tf.write(json.dumps(data, indent=4))
x=1
