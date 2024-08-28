from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.user import User, UserCredentials, UserPublic
from zupit.service.users_crud import (
    confirm_user_db,
    create_user_db,
    get_user_db,
)
from zupit.service.drivers_crud import get_driver_db

from zupit.utils import serialize_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_user(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(User.as_form),
):
    try:
        db_user = get_user_db(user.email, session)
        if db_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='User already exists'
            )

        db_user = create_user_db(user, session)
        request.session['user'] = serialize_user(db_user)
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
    session: Session = Depends(get_session),
    user: UserCredentials = Depends(UserCredentials.as_form),
) -> RedirectResponse:
    try:
        db_user = confirm_user_db(user, session)
        request.session['user'] = serialize_user(db_user)
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/sign-in', status_code=HTTPStatus.SEE_OTHER
        )


@router.get(
    '/{user_id}',
    response_model=UserPublic,
)
def get_user(user_id: int, session: Session = Depends(get_session)):
    db_user = get_user_db(user_id, session)

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


def is_driver(
    request: Request,
    user_id: int,
    session: Session = Depends(get_session),
) -> bool:
    driver = get_driver_db(user_id, session)
    if driver:
        request.session['driver'] = driver
        return True
    return False
