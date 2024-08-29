from zupit.router.users import get_user
from zupit.schemas.user import Public


def test_create_brazilian(client, session):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'icon': None,
    }
    payload = {
        **esperado,
        'password': '123',
        'nationality': 'BRAZILIAN',
        'cpf': '12345678900',
    }

    response = client.post('/users', data=payload)

    user_db = response.context['user']
    user = Public(**esperado, doc=payload['cpf'], id=user_db.id)

    assert response.template.name == 'search-travel.html'
    assert user_db == user


def test_create_foreigner(client, session):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'icon': None,
    }
    payload = {
        **esperado,
        'password': '123',
        'nationality': 'FOREIGNER',
        'rnm': '02140873',
    }

    response = client.post('/users', data=payload)

    id = response.context['request'].session['id']
    user_db = get_user(id, session)
    user = Public(**esperado, doc=payload['rnm'], id=id)

    assert response.template.name == 'search-travel.html'
    assert user_db == user


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
    assert response.context['request'].session['error'] == (
        'User already exists'
    )
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

    assert response.context['request'].session['error'] == ('Input invalid')
    assert response.template.name == 'sign-up.html'


def test_confirm_user_credentials(client, user):
    payload = {
        'email': user.email,
        'password': '123',
    }
    response = client.post('/users/confirm-user', data=payload)

    assert response.context['request'].session['id'] == user.id
    assert response.template.name == 'search-travel.html'


def test_wrong_emai_user_credentials(client, user):
    payload = {
        'email': 'wrongemail@example.com',
        'password': '123',
    }
    response = client.post('/users/confirm-user', data=payload)

    assert response.context['request'].session['error'] == ('User not found')
    assert response.template.name == 'sign-in.html'


def test_wrong_password_user_credentials(client, user):
    payload = {
        'email': user.email,
        'password': 'wrongpassword',
    }

    response = client.post('/users/confirm-user', data=payload)

    assert response.context['request'].session['error'] == ('User not found')
    assert response.template.name == 'sign-in.html'
