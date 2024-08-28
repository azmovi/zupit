from http import HTTPStatus

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from zupit.database import get_session
from zupit.router import drivers, users
from zupit.utils import get_user_from_request

app = FastAPI()

app.mount('/static', StaticFiles(directory='zupit/static'), name='static')
templates = Jinja2Templates(directory='zupit/templates')

app.add_middleware(SessionMiddleware, secret_key='secret_key')

app.include_router(users.router)
app.include_router(drivers.router)


@app.get('/', response_class=HTMLResponse)
def reset_session():
    return RedirectResponse(url='/logoff', status_code=HTTPStatus.SEE_OTHER)


@app.get('/logoff', response_class=HTMLResponse)
def logoff(request: Request):
    request.session.clear()
    return RedirectResponse(
        url='/search-travel', status_code=HTTPStatus.SEE_OTHER
    )


@app.get('/search-travel', response_class=HTMLResponse)
def search_travel(request: Request):
    user = request.session.get('user', None)
    error = request.session.get('error', None)
    return templates.TemplateResponse(
        request=request,
        name='search-travel.html',
        context={'user': user, 'error': error}
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
def offer(request: Request, session: Session = Depends(get_session)):
    if user := get_user_from_request(request):
        if users.is_driver(request, user.get(id, None), session):
            driver = request.session.get('driver', None)
            return templates.TemplateResponse(
                'offer.html',
                {'request': request, 'user': user, 'driver': driver},
            )
    return RedirectResponse(
        url='/create-driver', status_code=HTTPStatus.SEE_OTHER
    )


@app.get('/create-driver', response_class=HTMLResponse)
def create_driver(request: Request):
    user = request.session.get('user', None)
    error = request.session.get('error', None)

    return templates.TemplateResponse(
        request=request,
        name='create-driver.html',
        context={'user': user, 'error': error}
    )


@app.get('/car', response_class=HTMLResponse)
def car(request: Request):
    return templates.TemplateResponse('car.html', {'request': request})
