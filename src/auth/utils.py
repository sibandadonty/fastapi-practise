from passlib.context import CryptContext

password_ctx = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return password_ctx.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_ctx.verify(plain_password, hashed_password)
