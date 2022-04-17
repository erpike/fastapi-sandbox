import hashlib


from conf import SECRET_KEY


def get_password_hash(password: str):
    return hashlib.sha256(f"{SECRET_KEY}{password}".encode("utf8")).hexdigest()
