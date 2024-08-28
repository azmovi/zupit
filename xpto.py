from zupit.schemas.driver import Driver
from zupit.utils import serialize_driver

payload = {
    'name': 'Antonio',
    'email': 'antonio@example.com',
    'password': 'senha_secreta',
    'birthday': '2000-01-01',
    'sex': 'MAN',
    'nationality': 'BRAZILIAN',
    'cpf': '12345678900',
    'icon': None,
}

driver = Driver(user_id=1, cnh='123456789', rating=2.1, preferences=None)

print(serialize_driver(driver))


# response = requests.post('http://localhost:8000/users', json=payload)
# print(response.status_code)
# print(response.headers)
# print(response.text)
