from datetime import date
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from zupit.app import app
from zupit.database import get_session
from zupit.schemas import Gender, Nationality, Public, User
from zupit.service.users_crud import create_user_db


@pytest.fixture(scope='session')
def engine() -> Generator[Engine, None, None]:
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        yield _engine


@pytest.fixture
def session(engine: Engine):
    with engine.begin() as conn:
        init_db(conn, 'init.sql')

    with Session(engine) as session:
        yield session

    with engine.begin() as conn:
        trucate_db(conn)
    # drop all


def init_db(conn: Connection, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()[11:]
        conn.execute(text(sql_script))


def trucate_db(conn: Connection):
    sql = """
        SET session_replication_role = 'replica';

        SELECT tablename FROM pg_tables WHERE schemaname = 'schemaname';

        DO $$ DECLARE
            table_name TEXT;
        BEGIN
            FOR table_name IN (
                SELECT tablename
                FROM pg_catalog.pg_tables
                WHERE schemaname = 'schemaname'
            )
            LOOP

                EXECUTE 'TRUNCATE TABLE '
                || quote_ident(table_name)
                || ' CASCADE;';
            END LOOP;
        END $$;


        SET session_replication_role = 'origin';
    """
    conn.execute(text(sql))


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session) -> Public:
    user = User(
        name='antonio',
        email='antonio@example.com',
        password='123',
        birthday=date(2002, 7, 8),
        sex=Gender('MAN'),
        cpf='12345678900',
        nationality=Nationality('BRAZILIAN'),
    )
    user = create_user_db(user, session)
    return user
