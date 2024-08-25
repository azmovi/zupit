from http import HTTPStatus


def test_index_html_without_user(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'index.html'
    assert response.context['error'] is None


def test_index_html_with_user(client, user):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'index.html'
    assert response.context['error'] is None
    print(response.context['user'])


def test_form_sign_up_html(client):
    response = client.get('/sign-up')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-up.html'
    assert response.context['error'] is None


def test_form_sign_in_html(client):
    response = client.get('/sign-in')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-in.html'
    assert response.context['error'] is None


def test_logoff_user(client, user):
    response = client.get('/logoff')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'index.html'
    assert response.context['error'] is None
    assert response.context['user'] is None
