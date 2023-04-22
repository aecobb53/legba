
import datetime
import time
import json
import os
import yaml
# import threading

from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from bin.logger import Logger

logit = Logger(appname='legba_parse_ifsc', file_level='DEBUG', consol_level='DEBUG').return_loggit()

# Initilize
app = FastAPI()  # noqa
logit.debug('Done initilizing')


#############
# Endpoints #
#############


# Root
@app.get('/')
async def root(request: Request):
    """
    The home page has some explanation of what each tab does.
    Eventually it would be great to have picutres of the tabs here as well.
    """
    # logit.info('home endpoint hit')
    return {}

# Main Web Page for Andrew
@app.get('/main-page-andrew')
async def root(request: Request, response_class=HTMLResponse):
    """
    The home page has some explanation of what each tab does.
    Eventually it would be great to have picutres of the tabs here as well.
    """
    logit.info('Andrews main web page endpoint hit')

    with open('data/main_page.html', 'r') as hf:
        details = hf.read()
    
    return details
