from datetime import datetime, timedelta

import jwt

from test_site import settings


def get_token(user):
    access_payload = {
        'access_key': str(user.access_key),
        'email': user.email,
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token
