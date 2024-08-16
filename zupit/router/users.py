from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from zupit.database import Connection
from zupit.schemas import User, UserPublic
from zupit.service.users_crud import (
    create_brazilian,
    create_foreigner,
    get_user_by_email,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: User, conn: Connection):
    db_user = get_user_by_email(user.email, conn)

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Esse usuario ja está no banco',
        )

    if user.nationality.value == 'BRAZILIAN':
        db_user = create_brazilian(user, conn)
    else:
        db_user = create_foreigner(user, conn)

    return db_user
