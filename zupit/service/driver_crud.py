from http import HTTPStatus
from typing import Optional, Union

from fastapi import HTTPException

from zupit.database import Connection
from zupit.schemas import (
    Driver,
    Gender,
    Public,
    User,
    UserCredentials,
    UserPublic,
)


def get_driver_db(campo: Union[int, str], conn: Connection) -> Optional[UserPublic]:
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
            icon=user_db[5],
            doc=user_db[6],
        )
    return None


def create_user_db(user: User, conn: Connection):
    if user.nationality.value == 'BRAZILIAN':
        sql = 'SELECT * FROM create_brazilian(%s, %s, %s, %s, %s, %s);'
        doc = user.cpf
    else:
        sql = 'SELECT * FROM create_foreigner(%s, %s, %s, %s, %s, %s);'
        doc = user.rnm

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
                    doc,
                ),
            )
            user_db = cur.fetchone()
        except Exception:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
            )
    return Public(
        id=user_db[0],
        name=user_db[1],
        email=user_db[2],
        birthday=user_db[3],
        sex=Gender(user_db[4]),
        icon=user_db[5],
        doc=user_db[6],
    )


def confirm_user_db(user: UserCredentials, conn: Connection):
    sql = 'SELECT * FROM confirm_user(%s, %s)'
    with conn.cursor() as cur:
        try:
            cur.execute(sql, (user.email, user.password))
            user_db = cur.fetchone()
        except Exception:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='User not found'
            )
    return Public(
        id=user_db[0],
        name=user_db[1],
        email=user_db[2],
        birthday=user_db[3],
        sex=Gender(user_db[4]),
        icon=user_db[5],
        doc=user_db[6],
    )
