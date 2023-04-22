from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse


appname = 'borderlands'

app = FastAPI()

# Root
@app.get('/')
async def root(requests: Request):
    return {'Hello': 'WORLD!'}

@app.get('/main-page', response_class=HTMLResponse)
async def current_builds(requests: Request):
    with open('templates/main_page.html', 'r') as hf:
        html_content = hf.read()
    return HTMLResponse(content=html_content, status_code=200)
