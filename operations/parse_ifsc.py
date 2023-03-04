from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import phtml
import asyncio
import os


from requests_html import HTMLSession, AsyncHTMLSession


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

def get_current_rankings():
    # create an HTML Session object
    session = HTMLSession()

    resp_womens_lead = session.get(f"{ifsc_rankings}/5")
    resp_womens_lead.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_womens_lead.html', 'w') as hf:
        hf.write(resp_womens_lead.html.html)

    resp_womens_speed = session.get(f"{ifsc_rankings}/6")
    resp_womens_speed.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_womens_speed.html', 'w') as hf:
        hf.write(resp_womens_speed.html.html)

    resp_womens_boulder = session.get(f"{ifsc_rankings}/7")
    resp_womens_boulder.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_womens_boulder.html', 'w') as hf:
        hf.write(resp_womens_boulder.html.html)

    resp_womens_combined = session.get(f"{ifsc_rankings}/618")
    resp_womens_combined.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_womens_combined.html', 'w') as hf:
        hf.write(resp_womens_combined.html.html)

    resp_mens_lead = session.get(f"{ifsc_rankings}/1")
    resp_mens_lead.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_mens_lead.html', 'w') as hf:
        hf.write(resp_mens_lead.html.html)

    resp_mens_speed = session.get(f"{ifsc_rankings}/2")
    resp_mens_speed.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_mens_speed.html', 'w') as hf:
        hf.write(resp_mens_speed.html.html)

    resp_mens_boulder = session.get(f"{ifsc_rankings}/3")
    resp_mens_boulder.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_mens_boulder.html', 'w') as hf:
        hf.write(resp_mens_boulder.html.html)

    resp_mens_combined = session.get(f"{ifsc_rankings}/617")
    resp_mens_combined.html.render(sleep=1, keep_page=True, scrolldown=1)
    with open('rankings_mens_combined.html', 'w') as hf:
        hf.write(resp_mens_combined.html.html)

def parse_html_file(path):
    x=1
    hr = phtml.HtmlReader()
    fe = phtml.FindElement()
    doc = hr.read_file(path)[0]

    x=1
    elements = fe.find_elements(obj=doc, element_type=phtml.Div, _class='^athlete-basic-line$')
    deets = {}
    for el in elements[:10]:
        name = fe.find_elements(obj=el, element_type=phtml.Link, _class='r-name')[0].text.strip()
        rank = fe.find_elements(obj=el, element_type=phtml.Div, _class='rank')[0].text.strip()
        country = fe.find_elements(obj=el, element_type=phtml.Div, _class='r-name-sub')[0].text.strip()
        deets[name] = {
            'rank': rank,
            'country': country,
        }

    x=1

    path2 = 'deleteme.html'
    with open(path2, 'w') as hf:
        hf.write(doc.return_document)

    hr = phtml.HtmlReader()
    doc2 = hr.read_file(path2)
    with open('deleteme_2.html', 'w') as hf:
        hf.write(doc.return_document)
    x=1

get_current_rankings()

# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_mens_boulder.html'))
# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_mens_combined.html'))
# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_mens_lead.html'))
# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_mens_speed.html'))
parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_womens_boulder.html'))
# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_womens_combined.html'))
# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_womens_lead.html'))
# parse_html_file(path=os.path.join(os.getcwd(), 'operations', 'rankings_womens_speed.html'))

# # grab_rankings(ranking_extention='lead_women')
# hr = phtml.HtmlReader()
# # with open('data/ifsc_lead_women.html', 'r') as hf:
# x=1
# hr.read_file(filepath='data/ifsc_lead_women.html')
#     # html_data = hf.readlines()

# x=1
# grab_rankings(ranking_extention='lead_women')

# x=1
