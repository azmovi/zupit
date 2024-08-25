from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from zupit.database import Connection
from zupit.schemas import User, UserCredentials, UserPublic
from zupit.service.users_crud import (
    confirm_user_db,
    create_user_db,
    get_user_db,
)
from zupit.utils import serialize_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_user(
    request: Request,
    conn: Connection,
    user: User = Depends(User.as_form),
):
    try:
        db_user = get_user_db(user.email, conn)
        if db_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='User already exists'
            )

        db_user = create_user_db(user, conn)
        request.session['user'] = serialize_user(db_user)
        return RedirectResponse(url='/', status_code=HTTPStatus.SEE_OTHER)

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
    conn: Connection,
    user: UserCredentials = Depends(UserCredentials.as_form),
) -> RedirectResponse:
    try:
        db_user = confirm_user_db(user, conn)
        request.session['user'] = serialize_user(db_user)
        return RedirectResponse(url='/', status_code=HTTPStatus.SEE_OTHER)

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/sign-in', status_code=HTTPStatus.SEE_OTHER
        )


@router.get(
    '/{user_id}',
    response_model=UserPublic,
)
def get_user(user_id: int, conn: Connection):
    db_user = get_user_db(user_id, conn)

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user
