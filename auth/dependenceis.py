# file: app/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validate the JWT and retrieve the current user.
    """
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  # Return the payload (e.g., user ID)
