import json
from webbrowser import get
import requests

"""
https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c
"""
def get_stuff(url):
    resposne = requests.get(url)
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

# Broncos
code, data = get_stuff('https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/7/schedule')
# print(json.dumps(data, indent=2))
with open('deleteme.json', 'w') as tf:
    tf.write(json.dumps(data, indent=4))



x=1
