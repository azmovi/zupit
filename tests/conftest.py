import pytest
from psycopg import connect
from testcontainers.postgres import PostgresContainer


@pytest.fixture
def connection():
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        conn_url = postgres.get_connection_url()
        port = conn_url.split(':')[-1].split('/')[0]

        conn = connect(
            dbname='test',
            user='test',
            password='test',
            host='localhost',
            port=port,
        )

        cursor = conn.cursor()
        init(cursor, 'init.sql')

        yield conn, cursor

        conn.rollback()
        cursor.close()
        conn.close()


def init(cursor, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        cursor.execute(sql_script)
        cursor.connection.commit()
