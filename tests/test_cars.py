# import json
#
#
# def test_create_car(client, user):
#     esperado = {
#         'renavam': '12345678900',
#         'brand': 'fiat',
#         'model': 'mobi',
#         'plate': 'fjr5231',
#         'color': 'vermelho',
#     }
#
#     payload = {
#         **esperado,
#         'user_id': f'{user.id}',
#     }
#
#     response = client.post('/drivers', data=payload)
#
#     assert response.template.name == 'offer.html'
#     assert json.loads(response.context['driver']) == (
#         esperado | {'rating': '0.0', 'user_id': user.id}
#     )
#
#
# def test_create_driver_with_preferences(client, user):
#     esperado = {
#         'cnh': '123456789',
#         'preferences': 'Gosto de cachorro quente',
#     }
#
#     payload = {
#         **esperado,
#         'user_id': f'{user.id}',
#     }
#
#     response = client.post('/drivers', data=payload)
#
#     assert response.template.name == 'offer.html'
#     assert json.loads(response.context['driver']) == (
#         esperado | {'rating': '0.0', 'user_id': user.id}
#     )
#
#
# def test_create_foreigner(client):
#     esperado = {
#         'name': 'antonio',
#         'email': 'antonio@example.com',
#         'birthday': '2000-01-01',
#         'sex': 'MAN',
#         'icon': None,
#     }
#     payload = {
#         **esperado,
#         'password': '123',
#         'nationality': 'FOREIGNER',
#         'rnm': '02140873',
#     }
#
#     response = client.post('/users', data=payload)
#
#     assert response.template.name == 'search-travel.html'
#     assert json.loads(response.context['user']) == {
#         'id': 1,
#         'doc': payload['rnm'],
#         **esperado,
#     }
#
#
# def test_error_create_user_existent(client, user):
#     payload = {
#         'name': user.name,
#         'email': user.email,
#         'password': '123',
#         'birthday': '2002-07-08',
#         'sex': user.sex.value,
#         'cpf': user.doc,
#         'nationality': 'BRAZILIAN',
#     }
#     response = client.post('/users', data=payload)
#
#     assert response.context['error'] == 'User already exists'
#     assert response.template.name == 'sign-up.html'
#
#
# def test_create_user_invalid(client):
#     payload = {
#         'name': 'antonio',
#         'email': 'antonio@example.com',
#         'birthday': '2000-01-01',
#         'sex': 'MAN',
#         'cpf': '12345678900',
#         'password': '123',
#         'nationality': 'FOREIGNER',
#     }
#
#     response = client.post('/users', data=payload)
#
#     assert response.context['error'] == 'Input invalid'
#     assert response.template.name == 'sign-up.html'
#
#
# def test_confirm_user_credentials(client, user):
#     esperado = {
#         'id': 1,
#         'name': 'antonio',
#         'doc': user.doc,
#         'icon': None,
#         'birthday': '2002-07-08',
#         'sex': user.sex.value,
#     }
#     payload = {
#         'email': user.email,
#         'password': '123',
#     }
#     response = client.post('/users/confirm-user', data=payload)
#
#     assert response.template.name == 'search-travel.html'
#     assert json.loads(response.context['user']) == {
#         'email': user.email,
#         **esperado,
#     }
#
#
# def test_wrong_emai_user_credentials(client, user):
#     payload = {
#         'email': 'wrongemail@example.com',
#         'password': '123',
#     }
#     response = client.post('/users/confirm-user', data=payload)
#
#     assert response.context['error'] == 'User not found'
#     assert response.template.name == 'sign-in.html'
#
#
# def test_wrong_password_user_credentials(client, user):
#     payload = {
#         'email': user.email,
#         'password': 'wrongpassword',
#     }
#
#     response = client.post('/users/confirm-user', data=payload)
#
#     assert response.context['error'] == 'User not found'
#     assert response.template.name == 'sign-in.html'
