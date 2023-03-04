import requests
from bs4 import BeautifulSoup
import json
import phtml
import asyncio


from requests_html import HTMLSession, AsyncHTMLSession


ifsc_base_url = 'https://ifsc'
ifsc_rankings = f"{ifsc_base_url}.results.info/#/rankings/cuwr"


print('STARTING')
# create an HTML Session object
session = HTMLSession()

# # Use the object above to connect to needed webpage
# # resp = session.get("https://finance.yahoo.com/quote/NFLX/options?p=NFLX")
# resp = session.get('https://ifsc.results.info/#/rankings/cuwr/5')

# # Run JavaScript code on webpage
# resp.html.render(sleep=1, keep_page=True, scrolldown=1)

# with open('deleteme.html', 'w') as hf:
#     hf.write(resp.html.html)
# # url = f"{ifsc_rankings}/5"
# # print(url)


asession = AsyncHTMLSession()

async def get_womens_lead():
    r = asession.get(f"{ifsc_rankings}/5")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_womens_lead.html", 'w') as hf:
        hf.write(r.html.html)

async def get_womens_speed():
    r = asession.get(f"{ifsc_rankings}/6")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_womens_speed.html", 'w') as hf:
        hf.write(r.html.html)

async def get_womens_boulder():
    r = asession.get(f"{ifsc_rankings}/7")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_womens_boulder.html", 'w') as hf:
        hf.write(r.html.html)

async def get_womens_combined():
    r = asession.get(f"{ifsc_rankings}/618")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_womens_combined.html", 'w') as hf:
        hf.write(r.html.html)

async def get_mens_lead():
    r = asession.get(f"{ifsc_rankings}/1")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_mens_lead.html", 'w') as hf:
        hf.write(r.html.html)

async def get_mens_speed():
    r = asession.get(f"{ifsc_rankings}/2")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_mens_speed.html", 'w') as hf:
        hf.write(r.html.html)

async def get_mens_boulder():
    r = asession.get(f"{ifsc_rankings}/3")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_mens_boulder.html", 'w') as hf:
        hf.write(r.html.html)

async def get_mens_combined():
    r = asession.get(f"{ifsc_rankings}/617")
    await r.html.render(sleep=1, keep_page=True, scrolldown=1)

    with open(f"deleteme_mens_combined.html", 'w') as hf:
        hf.write(r.html.html)

# asession.run(get_womens_lead, get_womens_speed, get_womens_boulder, get_womens_combined, get_mens_lead, get_mens_speed, get_mens_boulder, get_mens_combined)
asession.run(get_womens_lead)
print('DONE')
