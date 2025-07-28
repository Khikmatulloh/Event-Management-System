from datetime import datetime, timedelta, timezone
from typing import Union

from jose import jwt,JWTError
from passlib.context import CryptContext
from app.settings import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(data: dict, expires_delta: Union[int, float, None] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta if expires_delta else ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
