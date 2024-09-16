from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.rate import Rate, RateList, RatePublic
from zupit.service.rate_crud import (
    create_rating_db,
    get_rates_by_user,
    get_rating_db,
    check_rating_db,
)
from zupit.utils import get_current_user

router = APIRouter(prefix='/rate', tags=['rate'])
templates = Jinja2Templates(directory='zupit/templates')


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_rating(
    request: Request,
    session: Session = Depends(get_session),
    rate: Rate = Depends(Rate.as_form),
) -> RedirectResponse:
    try:
        rating_db = check_rating_db(rate.author_id, rate.recipient_id, rate.rate_type, session)
        if rating_db:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Rate already exists'
            )
        rating = create_rating_db(rate, session)
        request.session['rate'] = rating
        return RedirectResponse(
            url='/profile/my-travels', status_code=HTTPStatus.SEE_OTHER
        )

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/profile/my-travels', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/{recipient_id}', response_model=RateList)
def get_rating_user(
    recipient_id: int, session: Session = Depends(get_session)
):
    if rate_list := get_rates_by_user(session, recipient_id):
        return rate_list
    return None


@router.get('/search/{rate_id}', response_model=RatePublic)
def get_rating(rate_id: int, session: Session = Depends(get_session)):
    db_rate = get_rating_db(rate_id, session)
    if db_rate:
        return db_rate
    return None


@router.get('/rate-driver/{user_id}', response_class=HTMLResponse)
def rate_driver(
    request: Request,
    user_id: int,
    session: Session = Depends(
        get_session
    ),  # Use Depends to inject the session
):
    user = get_current_user(
        request, session
    )  # Assuming this is a helper function in your code
    error = request.session.get('error', None)
    if user:
        return templates.TemplateResponse(
            name='rate/rate-driver.html',  # Path to the template
            context={
                'request': request,
                'user': user,
                'user_id': user_id,
                'error': error,
            },
        )
    return RedirectResponse(
        url='/profile/my-travels', status_code=HTTPStatus.SEE_OTHER
    )

@router.get('/rate-passenger/{user_id}', response_class=HTMLResponse)
def rate_driver(
    request: Request,
    user_id: int,
    session: Session = Depends(
        get_session
    ),  # Use Depends to inject the session
):
    user = get_current_user(
        request, session
    )  # Assuming this is a helper function in your code
    error = request.session.get('error', None)
    if user:
        return templates.TemplateResponse(
            name='rate/rate-passenger.html',  # Path to the template
            context={
                'request': request,
                'user': user,
                'user_id': user_id,
                'error': error,
            },
        )
    return RedirectResponse(
        url='/profile/my-travels', status_code=HTTPStatus.SEE_OTHER
    )
