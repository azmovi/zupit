from http import HTTPStatus
from types import resolve_bases

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from zupit.database import Connection
from zupit.router import drivers, users
from zupit.schemas import Public
from zupit.utils import get_user_from_request

app = FastAPI()

app.mount('/static', StaticFiles(directory='zupit/static'), name='static')
templates = Jinja2Templates(directory='zupit/templates')

app.add_middleware(SessionMiddleware, secret_key='secret_key')

app.include_router(users.router)
app.include_router(drivers.router)


@app.get('/', response_class=HTMLResponse)
def form_seach_travels(request: Request):
    user = get_user_from_request(request)
    error = request.session.get('error', None)
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={'user': user, 'error': error},
    )


@app.get('/sign-up', response_class=HTMLResponse)
def form_sign_up(request: Request):
    error = request.session.get('error', None)
    return templates.TemplateResponse(
        request=request, name='sign-up.html', context={'error': error}
    )


@app.get('/sign-in', response_class=HTMLResponse)
def form_sign_in(request: Request):
    error = request.session.get('error', None)
    return templates.TemplateResponse(
        request=request, name='sign-in.html', context={'error': error}
    )


@app.get('/offer', response_class=HTMLResponse)
def offer(request: Request, conn: Connection):
    user = get_user_from_request(request)
    if user := get_user_from_request(request):
        user = Public(**user)
        if driver := drivers.get_driver(user.id, conn):
            return templates.TemplateResponse(
                'offer.html',
                {'request': request, 'user': user, 'driver': driver},
            )

    return templates.TemplateResponse(
        'create-driver.html', {'request': request, 'user': user}
    )


@app.get('/car', response_class=HTMLResponse)
def car(request: Request):
    return templates.TemplateResponse(
        'car.html', {'request': request}
    )


@app.get('/logoff', response_class=HTMLResponse)
def logoff(request: Request):
    request.session.clear()
    return RedirectResponse(url='/', status_code=HTTPStatus.SEE_OTHER)
