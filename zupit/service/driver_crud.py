from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from zupit.database import Connection
from zupit.schemas import Driver, DriverPublic


def create_driver_db(driver: Driver, conn: Connection):
    sql = 'SELECT * FROM create_driver(%s, %s, %s);'

    with conn.cursor() as cur:
        try:
            cur.execute(
                sql,
                (
                    driver.user_id,
                    driver.cnh,
                    driver.preferences,
                ),
            )
            driver_db = cur.fetchone()
        except Exception:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
            )
    return DriverPublic(
        id=driver_db[0],
        cnh=driver_db[1],
        rating=driver_db[2],
        preferences=driver_db[3],
    )


def get_driver_db(user_id: int, conn: Connection) -> Optional[DriverPublic]:
    sql = 'SELECT * FROM get_driver(%s);'
    with conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        driver_db = cur.fetchone()

    if driver_db:
        return DriverPublic(
            id=driver_db[0],
            cnh=driver_db[1],
            rating=driver_db[2],
            preferences=driver_db[3],
        )
    return None
