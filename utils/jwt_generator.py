from datetime import timedelta, datetime
from jose import jwt

SECRET_KEY = 'some_long_string'
ALGORITHM = 'HS256'


def generate_jwt(username: str, user_id: int, expires: timedelta):

    exp_delta = datetime.now() + expires

    encode = {
        'sub': username,
        'id': user_id,
        'exp': exp_delta
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
