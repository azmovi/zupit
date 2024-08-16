from http import HTTPStatus


def test_create_brazilian(client):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'cpf': '12345678900',
    }
    payload = {**esperado, 'password': '123', 'nationality': 'BRAZILIAN'}

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, **esperado}


def test_create_foreigner(client):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'rnm': '02140873',
    }
    payload = {**esperado, 'password': '123', 'nationality': 'FOREIGNER'}

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, **esperado}


def test_error_create_user_existent(client, user):
    payload = {
        'name': user.name,
        'email': user.email,
        'password': '123',
        'birthday': '2002-07-08',
        'sex': user.sex.value,
        'cpf': user.cpf,
        'nationality': 'BRAZILIAN',
    }
    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Esse usuario ja está no banco'}


def test_create_foreigner_invalid(client):
    payload = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'cpf': '12345678900',
        'password': '123',
        'nationality': 'FOREIGNER',
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Input invalido'}


def test_create_brazilian_invalid(client):
    payload = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'rnm': '12345678',
        'password': '123',
        'nationality': 'BRAZILIAN',
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Input invalido'}
