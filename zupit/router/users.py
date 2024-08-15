from http import HTTPStatus

from fastapi import APIRouter

from zupit.database import Connection
from zupit.schemas import User, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: User, conn: Connection):
    pass
