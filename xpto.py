import json

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

# response = requests.post('http://localhost:8000/users', json=payload)
# print(response.status_code)
# print(response.headers)
# print(response.text)
a = json.dumps(payload)
print(a)
