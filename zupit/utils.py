import json

from zupit.schemas import Public


def serialize_user(user: Public):
    user_serialize = dict(user)
    user_serialize['birthday'] = user.birthday.isoformat()
    user_serialize['sex'] = user.sex.value
    return json.dumps(user_serialize)
