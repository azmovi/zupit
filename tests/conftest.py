from datetime import datetime, timezone
from typing import Generator, Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from zupit.app import app
from zupit.database import get_session
from zupit.router.drivers import get_driver
from zupit.schemas.cars import Car
from zupit.schemas.drivers import Driver
from zupit.schemas.travels import Address, Travel, TravelPublic
from zupit.schemas.users import Gender, Nationality, Public, User
from zupit.service.travels_crud import (
    create_address_db,
    create_travel_db,
    get_address_db,
    get_travel_db,
)
from zupit.service.users_crud import create_user_db, get_user_db


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
        conn.execute(text('DROP SCHEMA public CASCADE; CREATE SCHEMA public;'))


def init_db(conn: Connection, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()[11:]
        conn.execute(text(sql_script))


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(client) -> Public:
    user = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'password': '123',
        'nationality': 'BRAZILIAN',
        'cpf': '12345678900',
    }

    response = client.post('/users', data=user)
    return response.context['user']


@pytest.fixture
def user2(session) -> Public:
    user2 = User(
        name='Vitor',
        email='vitor@email.com',
        password='456',
        birthday='2002-03-02',
        sex=Gender('MAN'),
        nationality=Nationality('BRAZILIAN'),
        cpf='98765432144',
    )
    id = create_user_db(user2, session)
    user_db = get_user_db(id, session)

    return user_db


@pytest.fixture
def driver(client, user, session) -> Optional[Driver]:
    driver = {'user_id': user.id, 'cnh': '123456789', 'preferences': 'xpto'}

    client.post('/drivers', data=driver)
    return get_driver(user.id, session)


@pytest.fixture
def car1(client, user) -> Car:
    car = {
        'renavam': '12345678900',
        'user_id': user.id,
        'brand': 'fiat',
        'model': 'mobi',
        'plate': 'fjr5231',
        'color': 'vermelho',
    }

    client.post('/cars', data=car)
    return Car(**car)


@pytest.fixture
def car2(client, user) -> Car:
    car = {
        'renavam': '12345671929',
        'user_id': user.id,
        'brand': 'fiat',
        'model': 'argo',
        'plate': 'fsp9132',
        'color': 'azul',
    }

    client.post('/cars', data=car)
    return Car(**car)


@pytest.fixture
def origin(session, user):
    origin = Address(
        cep='13560-049',
        street='Rua Episcopal',
        district='Centro',
        city='São Carlos',
        state='SP',
        house_number='2423',
        direction='PICK_UP',
        user_id=user.id,
    )
    id = create_address_db(session, origin)
    address_db = get_address_db(session, id)

    return address_db


@pytest.fixture
def middle(session, user):
    middle = Address(
        cep='01313-020',
        street='Rua Doutor Plínio Barreto',
        district='Bela Vista',
        city='São Paulo',
        state='SP',
        house_number='123',
        direction='MIDDLE',
        user_id=user.id,
    )
    id = create_address_db(session, middle)
    address_db = get_address_db(session, id)

    return address_db


@pytest.fixture
def destination(session, user):
    destination = Address(
        cep='11040-050',
        street='Rua Conselheiro Ribas',
        district='Embaré',
        city='Santos',
        state='SP',
        house_number='234',
        direction='PICK_OFF',
        user_id=user.id,
    )
    id = create_address_db(session, destination)
    address_db = get_address_db(session, id)

    return address_db


def travel(session, user, origin, destination, car1) -> Optional[TravelPublic]:
    travel = Travel(
        user_id=user.id,
        renavam=car1.renavam,
        space=4,
        departure=datetime(2225, 2, 2, 5, 2, tzinfo=timezone.utc),
        origin=origin,
        middle=None,
        destination=destination,
    )
    id = create_travel_db(session, travel)
    return get_travel_db(session, id)


def full_travel(
    session, user, origin, middle, destination, car1
) -> Optional[TravelPublic]:
    travel = Travel(
        user_id=user.id,
        renavam=car1.renavam,
        space=4,
        departure=datetime(2225, 2, 2, 5, 2, tzinfo=timezone.utc),
        origin=origin,
        middle=middle,
        destination=destination,
    )
    id = create_travel_db(session, travel)
    return get_travel_db(session, id)
