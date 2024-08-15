import pytest
from fastapi.testclient import TestClient
from psycopg import connect
from testcontainers.postgres import PostgresContainer

from zupit.app import app
from zupit.database import get_db_conn


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
            autocommit=True,
        )

        cursor = conn.cursor()
        init(cursor, 'init.sql')

        yield conn

        conn.rollback()
        cursor.close()
        conn.close()


def init(cursor, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()[11:]
        cursor.execute(sql_script)
        cursor.connection.commit()


@pytest.fixture
def client(connection):
    def get_connection_override():
        return connection

    with TestClient(app) as client:
        app.dependency_overrides[get_db_conn] = get_connection_override
        yield client

    app.dependency_overrides.clear()
