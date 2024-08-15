from typing import Annotated

from fastapi import Depends
from psycopg import Connection, connect


def get_db_conn():
    conn = connect(
        dbname='zupit_db',
        user='postgres',
        password='postgres',
        host='zupit_database',
        port='5432',
        autocommit=True,
    )
    try:
        yield conn
    finally:
        conn.close()


Connection = Annotated[Connection, Depends(get_db_conn)]
