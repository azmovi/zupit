from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel

router = APIRouter(prefix='/travels', tags=['travels'])

Session = Annotated[Session, Depends(get_session)]

@router.post('/', response_model=bool)
def crate_travel(
    request: Request,
    session: Session,  #type: ignore
    travel: Travel
):
    if get_travel_


@router.get('/', response_model=bool)
def crate_travel(
    request: Request,
    session: Session,  #type: ignore
    travel: Travel
):
    return True
