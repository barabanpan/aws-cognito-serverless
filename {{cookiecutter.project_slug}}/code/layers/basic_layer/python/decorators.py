import json
import os
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import logging

from utils import response, unauthorized


REGION = os.environ.get("REGION")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")

keys_url = "https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(REGION, USER_POOL_ID)
with urllib.request.urlopen(keys_url) as f:
    keys = f.read()
keys = json.loads(keys.decode('utf-8'))['keys']


def verify_JWT_token(group):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # no authorization header, it's not bearer or no kid - unauthorized
            event = args[0]
            try:
                token = event["headers"]["Authorization"].split(" ")[1]  # Missing Authentication Token
                headers = jwt.get_unverified_headers(token)
                kid = headers.get("kid")
            except Exception as e:
                logging.warning(repr(e))
                return unauthorized()

            key_index = -1
            for i, key in enumerate(keys):
                if kid == key["kid"]:
                    key_index = i
                    break
            if key_index == -1:
                return unauthorized()  # Public key not found in jwks.json

            # something wrong with keys - unauthorized
            public_key = jwk.construct(keys[key_index])
            message, encoded_signature = str(token).rsplit('.', 1)
            decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
            if not public_key.verify(message.encode("utf8"), decoded_signature):
                return unauthorized()  # Signature verification failed

            claims = jwt.get_unverified_claims(token)
            if claims["token_use"] != "access":
                return unauthorized()

            if time.time() > claims["exp"]:
                return response(401, {"message": "The incoming token has expired"})

            # group is not the one - unauthorized to use this resource
            if group not in claims["cognito:groups"]:
                return response(403, {"message": "Forbidden"})

            res = func(*args, **kwargs)
            return res

        return wrapper

    return decorator
