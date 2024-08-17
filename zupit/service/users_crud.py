from http import HTTPStatus
from typing import Optional, Union

from fastapi import HTTPException

from zupit.database import Connection
from zupit.schemas import (
    Brazilian,
    Foreigner,
    Gender,
    Public,
    User,
    UserPublic,
)


def get_user(campo: Union[str, int], conn) -> Optional[UserPublic]:
    if isinstance(campo, int):
        sql = 'SELECT * FROM get_user_by_id(%s);'
    elif isinstance(campo, str):
        sql = 'SELECT * FROM get_user_by_email(%s);'

    with conn.cursor() as cur:
        cur.execute(sql, (campo,))
        user_db = cur.fetchone()

    if user_db:
        return Public(
            id=user_db[0],
            name=user_db[1],
            email=user_db[2],
            birthday=user_db[3],
            sex=Gender(user_db[4]),
            doc=user_db[5],
        )
    return None


def create_brazilian(user: User, conn: Connection):
    sql = 'SELECT * FROM create_brazilian(%s, %s, %s, %s, %s, %s);'
    with conn.cursor() as cur:
        try:
            cur.execute(
                sql,
                (
                    user.name,
                    user.email,
                    user.password,
                    user.birthday,
                    user.sex.value,
                    user.cpf,
                ),
            )
            user_db = cur.fetchone()
        except Exception:
            raise HTTPException(status_code=400, detail='Input invalid')

    return Brazilian(
        id=user_db[0],
        name=user_db[1],
        email=user_db[2],
        birthday=user_db[3],
        sex=Gender(user_db[4]),
        cpf=user_db[5],
    )


def create_foreigner(user: User, conn: Connection):
    sql = 'SELECT * FROM create_foreigner(%s, %s, %s, %s, %s, %s);'
    with conn.cursor() as cur:
        try:
            cur.execute(
                sql,
                (
                    user.name,
                    user.email,
                    user.password,
                    user.birthday,
                    user.sex.value,
                    user.rnm,
                ),
            )
            user_db = cur.fetchone()
        except Exception:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
            )

    return Foreigner(
        id=user_db[0],
        name=user_db[1],
        email=user_db[2],
        birthday=user_db[3],
        sex=Gender(user_db[4]),
        rnm=user_db[5],
    )
