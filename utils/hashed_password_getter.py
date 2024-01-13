from passlib.context import CryptContext


def get_hashed_password(password):

    crypt_context = CryptContext(schemes=['bcrypt'])
    return crypt_context.hash(password)


def get_crypt_context():
    return CryptContext(schemes=['bcrypt'])