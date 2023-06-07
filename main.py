import os
import logging

from logging.handlers import RotatingFileHandler
from logging import FileHandler  # , StreamHandler
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, ORJSONResponse

from parse_ifsc import search_ifsc_data
from classes.timecard import Timecard, POSTTimecardEntry

appname = 'legba'

# Logging
try:
    os.makedirs('logs')
except:
    pass
log_file = f"logs/{appname}.log"
logger = logging.getLogger('legba')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s - %(message)s', '%Y-%m-%dT%H:%M:%SZ')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

app = FastAPI()

# Root
@app.get('/')
async def root(requests: Request):
    logger.debug('GET on /')
    return {'Hello': 'WORLD!'}

# @app.get('/main-page', response_class=HTMLResponse)
# async def current_builds(requests: Request):
#     with open('templates/main_page.html', 'r') as hf:
#         html_content = hf.read()
#     return HTMLResponse(content=html_content, status_code=200)

# @app.get('/test-get', resource_class=HTMLResponse)
# async def test_get_endpoint(requests: Request):
#     return HTMLResponse(status_code=200)

# @app.get('/test-get-data', resource_class=HTMLResponse)
# async def test_get_endpoint(requests: Request):
#     data = {
#         'results': [
#             {}
#         ]
#     }
#     return HTMLResponse(status_code=200)

# @app.post('/test-post', resource_class=HTMLResponse)
# async def test_post_endpoint(requests: Request):
#     return HTMLResponse(status_code=200)

# @app.put('/test-put', resource_class=HTMLResponse)
# async def test_put_endpoint(requests: Request):
#     return HTMLResponse(status_code=200)

@app.get('/ifsc-data')
async def ifsc_current_rankings_data(requests: Request):
    logger.debug('GET on /ifsc-data')
    data = search_ifsc_data()
    content = {
        "data": data
    }
    return content


@app.get('/timecard')
async def timecard_get(requests: Request):
    logger.debug('GET on /timecard')
    tc = Timecard()
    x=1
    return {'get': 'timecard'}


@app.post('/timecard-entry')
async def timecard_post(requests: Request, timecard_entry: POSTTimecardEntry):
# async def timecard_post(requests: Request):
    logger.debug('POST on /timecard-entry')
    logger.debug(f"example: {timecard_entry.example}")
    tc = Timecard()
    x=1
    return {'post': 'timecard-entry', 'example': timecard_entry.example}
