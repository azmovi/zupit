from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from zupit.router import users
from zupit.schemas import User

app = FastAPI()

app.mount('/static', StaticFiles(directory='zupit/static'), name='static')
templates = Jinja2Templates(directory='zupit/templates')

app.include_router(users.router)


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get('user')
    return templates.TemplateResponse(
        'index.html',
        {'request': request, 'user': user}
    )

@app.get('/form', response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse('form.html', {'request': request})

@app.post('/submit', response_class=HTMLResponse)
def form_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    birthday: str = Form(...),
    sex: str = Form(...),
    nationality: str = Form(...),
    cpf: str = Form(None),
    rnm: str = Form(None),
):
    return templates.TemplateResponse('form.html', {'request': request})
