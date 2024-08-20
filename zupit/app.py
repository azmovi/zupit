import json
from http import HTTPStatus

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from zupit.database import Connection
from zupit.router import users
from zupit.router.users import confirm_user, create_user
from zupit.schemas import User, UserCredentials
from zupit.utils import serialize_user

app = FastAPI()

app.mount('/static', StaticFiles(directory='zupit/static'), name='static')
templates = Jinja2Templates(directory='zupit/templates')

app.add_middleware(SessionMiddleware, secret_key='secret_key')

app.include_router(users.router)


@app.get('/', response_class=HTMLResponse)
def form_seach_travels(request: Request):
    user = None
    try:
        user_json = request.session.get('user')
        if user_json:
            user = json.loads(user_json)
    except Exception:
        user = None

    return templates.TemplateResponse(
        request=request, name='index.html', context={'user': user}
    )


@app.get('/sign-up', response_class=HTMLResponse)
def form_sign_up(request: Request):
    return templates.TemplateResponse('sign-up.html', {'request': request})


@app.post('/sign-up', response_class=HTMLResponse)
def sign_up(
    request: Request,
    conn: Connection,
    user_form: User = Depends(User.as_form),
):
    user_db = create_user(user_form, conn)
    user_serialize = dict(user_db)
    user_serialize['birthday'] = user_db.birthday.isoformat()
    user_serialize['sex'] = user_db.sex.value
    request.session['user'] = json.dumps(user_serialize)

    return templates.TemplateResponse(
        'main.html', {'request': request, 'user': user_serialize}
    )


@app.get('/sign-in', response_class=HTMLResponse)
def form_sign_in(request: Request):
    return templates.TemplateResponse('sign-in.html', {'request': request})


@app.post('/sign-in', response_class=HTMLResponse)
def sign_in(
    request: Request,
    conn: Connection,
    credentials_form: UserCredentials = Depends(UserCredentials.as_form),
):
    user_db = confirm_user(credentials_form, conn)
    user = serialize_user(user_db)
    request.session['user'] = user

    return templates.TemplateResponse(
        'main.html', {'request': request, 'user': user}
    )


@app.get('/logoff', response_class=HTMLResponse)
def logoff(request: Request):
    request.session.clear()
    return RedirectResponse(url='/', status_code=HTTPStatus.SEE_OTHER)
