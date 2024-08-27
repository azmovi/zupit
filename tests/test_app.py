from http import HTTPStatus


def test_search_travel_html(client):
    response = client.get('/search-travel')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'search-travel.html'


def test_form_sign_up_html(client):
    response = client.get('/sign-up')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-up.html'


def test_form_sign_in_html(client):
    response = client.get('/sign-in')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-in.html'


def test_logoff_user(client):
    response = client.get('/logoff')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'search-travel.html'
