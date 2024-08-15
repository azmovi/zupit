from typing import Annotated

from fastapi import Depends
from psycopg import Connection, connect


def get_db_conn() -> Connection:
    conn = connect(
        dbname='zupit_db',
        user='root',
        password='root',
        host='localhost',
        port='5432',
        autocommit=True,
    )
    return conn


Connection = Annotated[Connection, Depends(get_db_conn)]
