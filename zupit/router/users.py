from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from zupit.database import Connection
from zupit.schemas import User, UserPublic
from zupit.service.users_crud import (
    create_brazilian,
    create_foreigner,
    get_user,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: User, conn: Connection):
    db_user = get_user(user.email, conn)

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User already in database',
        )

    if user.nationality.value == 'BRAZILIAN':
        db_user = create_brazilian(user, conn)
    else:
        db_user = create_foreigner(user, conn)

    return db_user


@router.get(
    '/{user_id}',
    response_model=UserPublic,
)
def read_user(user_id: int, conn: Connection):
    db_user = get_user(user_id, conn)

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user
