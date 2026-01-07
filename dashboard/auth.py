import os
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Checks if the user provided the correct username and password.
    Defaults: user="admin", pass="admin123" (if env vars not set)
    """
    # 1. Define valid credentials
    correct_username = os.environ.get("ADMIN_USER", "admin")
    correct_password = os.environ.get("ADMIN_PASS", "admin123")

    # 2. Check match securely (prevents timing attacks)
    is_user_ok = secrets.compare_digest(credentials.username, correct_username)
    is_pass_ok = secrets.compare_digest(credentials.password, correct_password)

    # 3. Reject if wrong
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username