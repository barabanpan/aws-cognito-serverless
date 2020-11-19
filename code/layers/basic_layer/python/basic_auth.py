from base64 import b64decode


class DecodeError(Exception):
    pass


def decode(encoded_str):
    """Decode an encrypted HTTP basic authentication string. Returns a tuple of
    the form (username, password), and raises a DecodeError exception if
    nothing could be decoded.
    """
    split = encoded_str.strip().split(' ')
    # If there are only two elements, check the first and ensure it says
    # 'basic' so that we know we're about to decode the right thing.
    if not (len(split) == 2 and split[0].strip().lower() == 'basic'):
        raise DecodeError
    try:
        username, password = b64decode(split[1]).decode().split(':', 1)
    except:  # noqa
        raise DecodeError
    return username, password
