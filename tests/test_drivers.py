from zupit.schemas.driver import Driver


def test_create_driver_without_preferences(client, user):
    esperado = {
        'cnh': '123456789',
        'preferences': None,
    }

    payload = {
        **esperado,
        'user_id': f'{user.id}',
    }

    response = client.post('/drivers', data=payload)
    driver_db = response.context['driver']
    driver = Driver(user_id=user.id, rating=0, **esperado)

    assert driver == driver_db
    assert response.template.name == 'offer.html'


def test_create_driver_with_preferences(client, user):
    esperado = {
        'cnh': '123456789',
        'preferences': 'Gosto de cachorro quente',
    }

    payload = {
        **esperado,
        'user_id': f'{user.id}',
    }

    response = client.post('/drivers', data=payload)

    driver_db = response.context['driver']
    driver = Driver(user_id=user.id, rating=0, **esperado)

    assert driver == driver_db
    assert response.template.name == 'offer.html'


# TODO Create invalid Driver
