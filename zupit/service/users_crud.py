from http import HTTPStatus

from fastapi import HTTPException

from zupit.database import Connection
from zupit.schemas import Brazilian, Foreigner, Gender, User


def get_user_by_email(email: str, conn: Connection) -> int | None:
    sql = 'SELECT * FROM get_user_by_email(%s);'
    id_user = None

    with conn.cursor() as cur:
        cur.execute(sql, (email,))
        result = cur.fetchone()

        if result:
            id_user = result[0]

    return id_user


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
            raise HTTPException(status_code=400, detail='Input invalido')

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
                status_code=HTTPStatus.BAD_REQUEST, detail='Input invalido'
            )

    return Foreigner(
        id=user_db[0],
        name=user_db[1],
        email=user_db[2],
        birthday=user_db[3],
        sex=Gender(user_db[4]),
        rnm=user_db[5],
    )
