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
