# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# SECRET_KEY = "super-secret-key"  # Change in production!
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)

# def hash_password(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def decode_token(token: str):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         return None

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "super-secret-key-change-in-production"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    # Use timezone-aware datetime
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_token(token: str) -> dict:
    """Verify if token is valid and not expired"""
    payload = decode_token(token)
    if payload is None:
        return None
    
    # Check if token has expired
    exp = payload.get("exp")
    if exp is None:
        return None
    
    if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
        return None
    
    return payload