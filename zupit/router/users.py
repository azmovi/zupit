from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from zupit.database import Connection
from zupit.schemas import Brazilian, User, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: User, conn: Connection):
    user_db = None
    breakpoint()
    if user.nationality.value == 'BRAZILIAN':
        try:
            sql = 'CALL create_brazilian(%s, %s, %s, %s, %s, %s);'
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    user.name,
                    user.email,
                    user.password,
                    user.birthday,
                    user.sex,
                    user.cpf,
                ),
            )
            user_db = cursor.fetchone()
            print(user_db)

            if user_db is None:
                raise HTTPException(
                    status_code=404, detail='User not created.'
                )

            return Brazilian(
                id=user_db[0],
                name=user_db[1],
                email=user_db[2],
                birthday=user_db[3],
                sex=user_db[4],
                cpf=user_db[5],
            )
        except Exception:
            raise HTTPException(status_code=500, detail='errei aqui')
        finally:
            cursor.close()
    else:
        raise HTTPException(
            status_code=402,
            detail=f'Unsupported nationality: {user.nationality}',
        )
