import os
import logging

from logging.handlers import RotatingFileHandler
from logging import FileHandler , StreamHandler
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from parse_ifsc import search_ifsc_data
from classes.timecard import Timecard, POSTTimecardEntry, PUTTimecard

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
if os.environ.get('STREAM_HANDLER', 'False') == 'True':
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

app = FastAPI()

# Setting up CORS and who can access the API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def timecard_get(requests: Request, day: str = None):
    logger.debug(f'day: {day}')
    logger.debug('GET on /timecard')
    tc = Timecard()
    return tc.display_data(day=day)


@app.put('/timecard')
async def timecard_put(requests: Request, timecard_data: PUTTimecard):
    logger.debug('PUT on /timecard')
    logger.debug(f"timecard_data: {timecard_data}")
    tc = Timecard()
    tc.save(data=timecard_data)
    return tc.data


@app.post('/timecard-set')
async def timecard_post(requests: Request, timecard_data: PUTTimecard):
    logger.debug('POST on /timecard-set')
    try:
        tc = Timecard()
        tc.save(data=timecard_data.put)
        logger.debug(f"Database overwritten")
    except Exception as err:
        logger.error(f"Internal Exception raised: {err}")
        return {'message': f"Internal Exception raised: {err}"}
    return tc.data


@app.post('/timecard-entry')
async def timecard_post(requests: Request, timecard_entry: POSTTimecardEntry):
    logger.debug('POST on /timecard-entry')
    try:
        tc = Timecard()
        entry = timecard_entry.return_timecard_entry()
        entry.validate_im_good()
        tc.add_entry(entry=entry)
        tc.save()
    except ValueError as err:
        logger.warning(f"{err}")
        raise HTTPException(status_code=500, detail=f"{err}")
    except Exception as err:
        logger.warning(f"{err}")
        raise HTTPException(status_code=500, detail=f"{err}")
    return entry.put

@app.put('/timecard-entry/{recordId}')
async def timecard_post(requests: Request, recordId: str, timecard_entry: POSTTimecardEntry):
    logger.debug('PUT on /timecard-entry')
    logger.debug('I STILL NEED TO WRITE PUT LOGIC')
    try:
        tc = Timecard()
        entry = timecard_entry.return_timecard_entry()
        entry.validate_im_good()
        tc.add_entry(entry=entry)
        tc.save()
    except ValueError as err:
        logger.warning(f"{err}")
        raise HTTPException(status_code=500, detail=f"{err}")
    except Exception as err:
        logger.warning(f"{err}")
        raise HTTPException(status_code=500, detail=f"{err}")
    return entry.put

