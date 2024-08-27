from datetime import date
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session, sessionmaker
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
    with engine.connect() as conn:
        init_db(conn, 'init.sql')

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


def init_db(conn: Connection, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()[11:]
        conn.execute(text(sql_script))


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
