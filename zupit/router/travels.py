from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel, TravelList, TravelPublic
from zupit.service.travels_crud import (  # get_travel_by_user
    create_travel_db,
    get_travel_by_user,
    get_travel_db,
)

router = APIRouter(prefix='/travels', tags=['travels'])

Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def crate_travel(
    request: Request,
    session: Session,  # type: ignore
    travel: Travel,
):
    try:
        create_travel_db(session, travel)
        return RedirectResponse(
            url='/profile/', status_code=HTTPStatus.SEE_OTHER
        )
    except HTTPException as exc:
        request.session['error'] = exc.detail
        print(request.session)
        return RedirectResponse(
            url='/offer/fifth', status_code=HTTPStatus.SEE_OTHER
        )

@router.get('/{user_id}/', response_model=TravelList)
def get_travel(
    session: Session,  # type: ignore
    user_id: int,
):
    if travel_list := get_travel_by_user(session, user_id):
        return travel_list
    return None

@router.get('/search/{travel_id}/', response_model=TravelPublic)
def get_travel(
    session: Session,  # type: ignore
    travel_id: int,
):
    if specific_travel := get_travel_db(session, travel_id):
        return specific_travel
    return None
