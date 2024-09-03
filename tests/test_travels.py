from zupit.schemas.travels import Address
from zupit.service.travels_crud import create_address_db


def test_create_address(session, user):
    address = Address(
        cep='68015-540',
        street='Beco São Carlos',
        district='Urumari',
        city='Santarém',
        state='PA',
        house_number='1234',
        direction='PICK_UP',
        user_id=user.id,
    )
    id = create_address_db(session, address)

    assert id == 1
