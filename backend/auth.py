import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, HTTPException, Depends
from .database import get_db

# Security configuration
SECRET_KEY = os.environ.get("JWT_SECRET", "super-secret-placeholder-for-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

pwd_context = None # Moved to security.py

from .security import verify_password, get_password_hash

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, db = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    async with db.execute("SELECT id, username FROM users WHERE username = ?", (username,)) as cursor:
        user = await cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": user["id"], "username": user["username"]}
