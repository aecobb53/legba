from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, ORJSONResponse

from parse_ifsc import search_ifsc_data
from .classes.timecard import Timecard

appname = 'borderlands'

app = FastAPI()

# Root
@app.get('/')
async def root(requests: Request):
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
    data = search_ifsc_data()
    content = {
        "data": data
    }
    return content


@app.get('/timecard')
async def timecard_get(requests: Request):
    tc = Timecard()
    return {'get': 'timecard'}


@app.post('/timecard-entry')
async def timecard_get(requests: Request):
    tc = Timecard()
    return {'post': 'timecard-entry'}

