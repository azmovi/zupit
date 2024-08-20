from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from zupit.database import Connection
from zupit.schemas import User, UserCredentials, UserPublic
from zupit.service.users_crud import (
    confirm_user_db,
    create_user_db,
    get_user_db,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: User, conn: Connection):
    db_user = get_user_db(user.email, conn)

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User already in database',
        )
    db_user = create_user_db(user, conn)
    return db_user


@router.post(
    '/confirm',
    response_model=UserPublic,
)
def confirm_user(user: UserCredentials, conn: Connection):
    db_user = confirm_user_db(user, conn)
    return db_user


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
