from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel
from zupit.service.travels_crud import create_travel_db, valid_travel

router = APIRouter(prefix='/travels', tags=['travels'])

Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=bool)
def crate_travel(
    request: Request,
    session: Session,  # type: ignore
    travel: Travel,
):
    try:
        if valid_travel(session, session):
            create_travel_db(session, travel)
        else:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Impossible execute this travel',
            )
        return True
    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/sign-up', status_code=HTTPStatus.SEE_OTHER
        )
