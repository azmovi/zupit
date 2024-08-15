from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from zupit.router import users

app = FastAPI()

app.mount('/static', StaticFiles(directory='zupit/static'), name='static')
templates = Jinja2Templates(directory='zupit/templates')

app.include_router(users.router)


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/form', response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse('form.html', {'request': request})
