from http import HTTPStatus


def test_create_brazilian(client):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
    }
    payload = {
        **esperado,
        'password': '123',
        'nationality': 'BRAZILIAN',
        'cpf': '12345678900',
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'icon': None,
        'doc': payload['cpf'],
        **esperado,
    }


def test_create_foreigner(client):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
    }
    payload = {
        **esperado,
        'password': '123',
        'nationality': 'FOREIGNER',
        'icon': 'None',
        'rnm': '02140873',
    }

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'icon': None,
        'doc': payload['rnm'],
        **esperado,
    }


def test_error_create_user_existent(client, user):
    payload = {
        'name': user.name,
        'email': user.email,
        'password': '123',
        'birthday': '2002-07-08',
        'sex': user.sex.value,
        'cpf': user.doc,
        'nationality': 'BRAZILIAN',
    }
    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'User already in database'}


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
    assert response.json() == {'detail': 'Input invalid'}


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
    assert response.json() == {'detail': 'Input invalid'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')
    esperado = {
        'id': 1,
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2002-07-08',
        'sex': 'MAN',
        'doc': '12345678900',
        'icon': None,
    }
    assert response.status_code == HTTPStatus.OK
    assert response.json() == esperado


def test_get_user_not_exist(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_confirm_user_credentials(client, user):
    esperado = {
        'id': 1,
        'name': 'antonio',
        'doc': user.doc,
        'icon': None,
        'birthday': '2002-07-08',
        'sex': user.sex.value,
    }
    payload = {
        'email': user.email,
        'password': '123',
    }
    response = client.post('/users/confirm', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {**esperado, 'email': user.email}


def test_wrong_emai_user_credentials(client, user):
    payload = {
        'email': 'wrongemail@example.com',
        'password': '123',
    }
    response = client.post('/users/confirm', json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_wrong_password_user_credentials(client, user):
    payload = {
        'email': user.email,
        'password': 'wrongpassword',
    }
    response = client.post('/users/confirm', json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
