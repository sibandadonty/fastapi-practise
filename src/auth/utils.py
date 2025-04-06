from passlib.context import CryptContext

passlib_ctx = CryptContext(
    schemes=["bcrypt"]
)

def hash_password(password: str):
    return passlib_ctx.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return passlib_ctx.verify(plain_password, hashed_password)
