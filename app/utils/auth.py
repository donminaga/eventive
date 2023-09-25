# utils/auth.py

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

security = HTTPBearer()


def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")
