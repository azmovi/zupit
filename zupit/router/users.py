from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.user import User, UserCredentials, UserPublic
from zupit.service.drivers_crud import get_driver_db
from zupit.service.users_crud import (
    confirm_user_db,
    create_user_db,
    get_user_db,
)

router = APIRouter(prefix='/users', tags=['users'])

FUser = Annotated[User, Depends(User.as_form)]
CUser = Annotated[UserCredentials, Depends(UserCredentials.as_form)]
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_user(
    request: Request,
    session: Session,
    user: FUser,
):
    try:
        db_user = get_user_db(user.email, session)
        if db_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='User already exists'
            )

        id = create_user_db(user, session)
        request.session['id'] = id
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/sign-up', status_code=HTTPStatus.SEE_OTHER
        )


@router.post(
    '/confirm-user',
    response_class=HTMLResponse,
)
def confirm_user(
    request: Request,
    session: Session,
    user: CUser,
) -> RedirectResponse:
    try:
        id = confirm_user_db(user, session)
        request.session['id'] = id
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/sign-in', status_code=HTTPStatus.SEE_OTHER
        )


def get_user(user_id: int, session: Session) -> Optional[UserPublic]:
    db_user = get_user_db(user_id, session)

    if db_user := get_user_db(user_id, session):
        return db_user

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found'
    )


def is_driver(user_id: int, session: Session) -> bool:
    if get_driver_db(user_id, session):
        return True
    return False
