from datetime import date

import pytest
from fastapi.testclient import TestClient
from psycopg import connect
from testcontainers.postgres import PostgresContainer

from zupit.app import app
from zupit.database import get_db_conn
from zupit.router.users import create_user
from zupit.schemas import Gender, Nationality, Public, User


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


@pytest.fixture
def user(connection) -> Public:
    user = User(
        name='antonio',
        email='antonio@example.com',
        password='123',
        birthday=date(2002, 7, 8),
        sex=Gender('MAN'),
        cpf='12345678900',
        nationality=Nationality('BRAZILIAN'),
    )
    user = create_user(user, connection)
    return user
