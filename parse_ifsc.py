from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import phtml
import asyncio
import os

from classes.ifsc import AthleteProfile, Event, Gender, EventType
from requests_html import HTMLSession, AsyncHTMLSession



from classes.wall import Wall
from classes.mosaic import Mosaic, TrafficMosaic, IFSCMosaic
from classes.tile import TargetElement, LinkElement, Tile
from phtml import *

from bin.logger import Logger



ifsc_base_url = 'https://ifsc'
ifsc_rankings = f"{ifsc_base_url}.results.info/#/rankings/cuwr"

rankings_extentions = {
    'lead_men': 1,
    'speed_men': 2,
    'boulder_men': 3,
    'combined_men': 617,
    'lead_women': 5,
    'speed_women': 6,
    'boulder_women': 7,
    'combined_women': 618,
}

def get_current_rankings(logit):
    # create an HTML Session object
    directory_path = 'data/rankings'
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    logit.info('About to grab current rankings')
    session = HTMLSession()

    resp_womens_lead = session.get(f"{ifsc_rankings}/5")
    resp_womens_lead.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_womens_lead_path = f'{directory_path}/womens_lead.html'
    with open(resp_womens_lead_path, 'w') as hf:
        hf.write(resp_womens_lead.html.html)
    logit.debug(f"resp_womens_lead updated: {resp_womens_lead_path}")

    resp_womens_speed = session.get(f"{ifsc_rankings}/6")
    resp_womens_speed.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_womens_speed_path = f'{directory_path}/womens_speed.html'
    with open(resp_womens_speed_path, 'w') as hf:
        hf.write(resp_womens_speed.html.html)
    logit.debug(f"resp_womens_speed updated: {resp_womens_speed_path}")

    resp_womens_boulder = session.get(f"{ifsc_rankings}/7")
    resp_womens_boulder.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_womens_boulder_path = f'{directory_path}/womens_boulder.html'
    with open(resp_womens_boulder_path, 'w') as hf:
        hf.write(resp_womens_boulder.html.html)
    logit.debug(f"resp_womens_boulder updated: {resp_womens_boulder_path}")

    resp_womens_combined = session.get(f"{ifsc_rankings}/618")
    resp_womens_combined.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_womens_combined_path = f'{directory_path}/womens_combined.html'
    with open(resp_womens_combined_path, 'w') as hf:
        hf.write(resp_womens_combined.html.html)
    logit.debug(f"resp_womens_combined updated: {resp_womens_combined_path}")

    resp_mens_lead = session.get(f"{ifsc_rankings}/1")
    resp_mens_lead.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_mens_lead_path = f'{directory_path}/mens_lead.html'
    with open(resp_mens_lead_path, 'w') as hf:
        hf.write(resp_mens_lead.html.html)
    logit.debug(f"resp_mens_lead updated: {resp_mens_lead_path}")

    resp_mens_speed = session.get(f"{ifsc_rankings}/2")
    resp_mens_speed.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_mens_speed_path = f'{directory_path}/mens_speed.html'
    with open(resp_mens_speed_path, 'w') as hf:
        hf.write(resp_mens_speed.html.html)
    logit.debug(f"resp_mens_speed updated: {resp_mens_speed_path}")

    resp_mens_boulder = session.get(f"{ifsc_rankings}/3")
    resp_mens_boulder.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_mens_boulder_path = f'{directory_path}/mens_boulder.html'
    with open(resp_mens_boulder_path, 'w') as hf:
        hf.write(resp_mens_boulder.html.html)
    logit.debug(f"resp_mens_boulder updated: {resp_mens_boulder_path}")

    resp_mens_combined = session.get(f"{ifsc_rankings}/617")
    resp_mens_combined.html.render(sleep=2, keep_page=True, scrolldown=1)
    resp_mens_combined_path = f'{directory_path}/mens_combined.html'
    with open(resp_mens_combined_path, 'w') as hf:
        hf.write(resp_mens_combined.html.html)
    logit.debug(f"resp_mens_combined updated: {resp_mens_combined_path}")

    logit.info('Done getting current IFSC rankings')

def parse_html_file(path, logit):
    logit.info(f'About to parse html file: {path}')
    hr = phtml.HtmlReader()
    fe = phtml.FindElement()
    doc = hr.read_file(path)[0]

    elements = fe.find_elements(obj=doc, element_type=phtml.Div, _class='^athlete-basic-line$')
    athletes = []
    for el in elements[:20]:  # This should be updated to more than the first 10 probably
        name = fe.find_elements(obj=el, element_type=phtml.Link, _class='r-name')[0].text.strip()
        rank = fe.find_elements(obj=el, element_type=phtml.Div, _class='rank')[0].text.strip()
        country = fe.find_elements(obj=el, element_type=phtml.Div, _class='r-name-sub')[0].text.strip()

        event = os.path.basename(path).split('.')[0]
        if 'women' in event:
            gender = Gender.WOMEN
        elif 'men' in event:
            gender = Gender.MEN

        if 'lead' in event:
            event_type = EventType.LEAD
        elif 'boulder' in event:
            event_type = EventType.BOULDER
        elif 'speed' in event:
            event_type = EventType.SPEED
        elif 'combined' in event:
            event_type = EventType.COMBINED

        event = Event(
            event=event_type,
            rank=int(rank),
        )
        athlete = AthleteProfile(
            name=name,
            country=country,
            gender=gender,
            events=[event]
        )
        athletes.append(athlete)
    logit.info(f'Done parse html file: {path}')
    return athletes

def make_mosaic_file(athlete_list, logit):
    """
    1. Make a list for each even in order of athlete rank
    2. Create a tile for each event and a tile for each athletes (At least i think ill nead 2 tiles)
    3. Add to mosaic
    4. generate HTML
    5. Serve html
    6. Verify the crontab works
    """

    events = {}

    logit.info('About to create a mosaic from athletes data')

    for athlete in athlete_list:
        for event in athlete.events:
            event_name = f"{athlete.gender.value}s {event.event.value}"
            if event_name not in events:
                events[event_name] = []
            events[event_name].append({
                'athlete_name': athlete.name,
                'athlete_rank': event.rank,
                'athlete': athlete,
            })

    event_list = [
        {'event': 'womens lead', 'name': 'WL', 'description': 'Womens Lead'},
        {'event': 'womens boulder', 'name': 'WB', 'description': 'Womens Bouldering'},
        {'event': 'womens speed', 'name': 'WS', 'description': 'Womens Speed'},
        {'event': 'womens combined', 'name': 'WC', 'description': 'Womens Combined'},
        {'event': 'mens lead', 'name': 'ML', 'description': 'Mens Lead'},
        {'event': 'mens boulder', 'name': 'MB', 'description': 'Mens Bouldering'},
        {'event': 'mens speed', 'name': 'MS', 'description': 'Mens Speed'},
        {'event': 'mens combined', 'name': 'MC', 'description': 'Mens Combined'},
    ]

    ifsc_mosaic = IFSCMosaic()
    for event_item in event_list:
        athletes = events[event_item['event']]
        athletes.sort(key=lambda x: x['athlete_rank'])
        content = phtml.HtmlList(ordered=True)
        for athlete in athletes[:5]:
            item = phtml.HtmlListItem(
                content=f"{athlete['athlete_rank']} {athlete['athlete_name']} {athlete['athlete'].country}"
            )
            content.add_element(obj=item)
        x=1
        tile = Tile(
            name=event_item['name'],
            description=event_item['description'],
            content=content.return_string_version,
            html_classes=['tile-ifsc']
        )
        ifsc_mosaic.tiles.append(tile)
    logit.info('Done creating ifsc mosaic')
    return ifsc_mosaic
        

if __name__ == '__main__':
    needed_infrastructure = [
        'logs',
        'data/rankings',
    ]
    for dir in needed_infrastructure:
        if not os.path.exists(dir):
            os.makedirs(dir)

    logit = Logger(appname='legba_parse_ifsc', file_level='DEBUG', consol_level='DEBUG').return_loggit()

    # get_current_rankings(logit=logit)

    # all_athletes = []
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'mens_boulder.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'mens_combined.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'mens_lead.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'mens_speed.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'womens_boulder.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'womens_combined.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'womens_lead.html'), logit=logit))
    # all_athletes.extend(parse_html_file(path=os.path.join(os.getcwd(), 'data', 'rankings', 'womens_speed.html'), logit=logit))

    # condenced_dct = {}
    # for athlete in all_athletes:
    #     if athlete.name not in condenced_dct:
    #         condenced_dct[athlete.name] = athlete
    #     else:
    #         condenced_dct[athlete.name].events.extend(athlete.events)
    #     x=1

    ifsc_rankings_path = 'data/ifsc_rankings.json'
    # logit.info(f'About to write the {ifsc_rankings_path} file')
    # with open(ifsc_rankings_path, 'w') as tf:
    #     tf.write(json.dumps([a.put for a in condenced_dct.values()], indent=4))

    with open(ifsc_rankings_path, 'r') as tf:
        temp_athletes = json.load(tf)
    logit.info(f'Done writing the {ifsc_rankings_path} file')

    athletes = []
    for item in temp_athletes:
        athletes.append(AthleteProfile.build(item))

    ifsc_mosaic = make_mosaic_file(athlete_list=athletes, logit=logit)
    x=1

    ifsc_mosaic_path = 'data/ifsc_mosaic.json'
    logit.info(f'About to write the {ifsc_mosaic_path} file')
    with open(ifsc_mosaic_path, 'w') as tf:
        tf.write(json.dumps(ifsc_mosaic.put, indent=4))

    x=1

# make_mosaic_file(athlete_list=[a.put for a in condenced_dct.values()])

"""
apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
"""