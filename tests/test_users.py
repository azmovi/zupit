from http import HTTPStatus


def test_create_brazilian(client):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'sex': 'MAN',
        'nacionality': 'FOREIGNER',
        'cpf': '25510057244',
    }
    payload = {**esperado, 'password': '123'}

    response = client.post('/users', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, **esperado}
