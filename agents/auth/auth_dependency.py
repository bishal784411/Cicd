from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from auth.auth_handler import verify_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    access_token: Optional[str] = Cookie(None)
):
    """
    Get current user from JWT token (either from Authorization header or cookie)
    """
    token = None
    
    # Try to get token from Authorization header first
    if credentials:
        token = credentials.credentials
    # If no Authorization header, try to get from cookie
    elif access_token:
        token = access_token
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return email

def get_current_active_user(current_user: str = Depends(get_current_user)):
    """
    Get current active user (can add additional validation here)
    """
    # You can add additional checks here like:
    # - Check if user is active in database
    # - Check user permissions
    # - etc.
    return current_user

# Optional: Create a dependency that doesn't require authentication (for optional auth)
def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    access_token: Optional[str] = Cookie(None)
) -> Optional[str]:
    """
    Get current user but don't raise exception if not authenticated
    Returns None if not authenticated
    """
    token = None
    
    if credentials:
        token = credentials.credentials
    elif access_token:
        token = access_token
    
    if not token:
        return None
    
    payload = verify_token(token)
    if payload is None:
        return None
    
    return payload.get("sub")