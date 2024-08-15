from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, HTTPException

from zupit.database import Connection
from zupit.schemas import Brazilian, Foreigner, User

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=Union[Brazilian, Foreigner],
    status_code=HTTPStatus.CREATED,
)
def create_user(user: User, conn: Connection):
    user_db = None
    if user.nationality == 'BRAZILIAN':
        try:
            sql = """
            CALL create_brazilian(
                :name,
                :email,
                :password,
                :birthday,
                :sex,
                :cpf
            );
            """
            result = conn.execute(
                sql,
                {
                    'name': user.name,
                    'emai': user.email,
                    'password': user.password,
                    'birthday': user.birthday,
                    'sex': user.sex,
                    'cpf': user.cpf,
                },
            )
            user_db = result.fetchone()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            return user_db
    else: 
        raise HTTPException(
            status_code=402, detail=f'outra coisa {user.nationality}'
        )
