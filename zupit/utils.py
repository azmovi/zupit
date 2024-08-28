import json

from fastapi import Request

from zupit.schemas.driver import Driver
from zupit.schemas.user import UserPublic


def serialize_user(user: UserPublic):
    user_serialize = dict(user)
    user_serialize['birthday'] = user.birthday.isoformat()
    user_serialize['sex'] = user.sex.value
    return json.dumps(user_serialize)


def serialize_driver(driver: Driver):
    dict_driver = dict(driver)
    if dict_driver['rating'] == 0.0:
        dict_driver['rating'] = 0
    return json.dumps(dict_driver)


def get_user_from_request(request: Request):
    user_json = request.session.get('user')
    if user_json:
        return json.loads(user_json)
    return None
