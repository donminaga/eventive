from fastapi import APIRouter, HTTPException, Header

from app.models import UserRegistration, UserLogin
from firebase_admin import auth

router = APIRouter()


@router.post("/register")
def register(user: UserRegistration):
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        return {"uid": user_record.uid, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    try:
        user_record = auth.get_user_by_email(user.email)
        custom_token = auth.create_custom_token(user_record.uid)
        return {"token": custom_token, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")
