from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generate a new JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    Decode and verify the JWT token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
