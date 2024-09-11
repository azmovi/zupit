from zupit.schemas.cars import Car
from zupit.schemas.travels import Address
from zupit.schemas.users import Public


def test_create_travel(
    client,
    user: Public,
    car1: Car,
    origin: Address,
    middle: Address,
    destination: Address,
):
    data = {
        'user_id': user.id,
        'renavam': car1.renavam,
        'space': '4',
        'departure': '2025-10-11T11:00:00.000Z',
        'origin': {
            'user_id': origin.user_id,
            'direction': origin.direction,
            'cep': origin.cep,
            'street': origin.street,
            'district': origin.district,
            'city': origin.city,
            'state': origin.state,
            'house_number': origin.house_number,
        },
        'middle': {
            'user_id': middle.user_id,
            'direction': middle.direction,
            'cep': middle.cep,
            'street': middle.street,
            'district': middle.district,
            'city': middle.city,
            'state': middle.state,
            'house_number': middle.house_number,
        },
        'destination': {
            'user_id': destination.user_id,
            'direction': destination.direction,
            'cep': destination.cep,
            'street': destination.street,
            'district': destination.district,
            'city': destination.city,
            'state': destination.state,
            'house_number': destination.house_number,
        },
    }

    response = client.post('/travels', json=data)

    assert response.template.name == 'profile/index.html'
