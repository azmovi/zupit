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
        'icon': 'None',
        'cpf': '12345678900',
    }

    response = client.post('/users', data=payload)

    assert response.template.name == 'index.html'
    assert response.context['user'] == {
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
        'rnm': '02140873',
    }

    response = client.post('/users', data=payload)

    assert response.template.name == 'index.html'
    assert response.context['user'] == {
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
    response = client.post('/users', data=payload)

    assert response.context['error'] == 'User already exists'
    assert response.template.name == 'sign-up.html'


def test_create_user_invalid(client):
    payload = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'cpf': '12345678900',
        'password': '123',
        'nationality': 'FOREIGNER',
    }

    response = client.post('/users', data=payload)

    assert response.context['error'] == 'Input invalid'
    assert response.template.name == 'sign-up.html'


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
    response = client.post('/users/confirm-user', data=payload)

    assert response.template.name == 'index.html'
    assert response.context['user'] == {
        'email': user.email,
        **esperado,
    }


def test_wrong_emai_user_credentials(client, user):
    payload = {
        'email': 'wrongemail@example.com',
        'password': '123',
    }
    response = client.post('/users/confirm', json=payload)

    assert response.json() == {'detail': 'User not found'}


def test_wrong_password_user_credentials(client, user):
    payload = {
        'email': user.email,
        'password': 'wrongpassword',
    }
    response = client.post('/users/confirm', json=payload)

    assert response.json() == {'detail': 'User not found'}
