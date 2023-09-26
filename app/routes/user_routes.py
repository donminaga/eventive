from fastapi import APIRouter, HTTPException, Header

from app.models import UserRegistration, UserLogin
from firebase_admin import auth, firestore, credentials, initialize_app
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, '../firebase-credentials.json')
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)

initialize_app(cred)

db = firestore.client()
router = APIRouter()


@router.post("/register")
def register(user: UserRegistration):
    try:
        # Create user in Firebase Authentication
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )

        custom_token = auth.create_custom_token(user_record.uid)

        # Save user details in Firestore
        user_data = {
            "name": user.name,
            "email": user.email
        }
        db.collection("users").document(user_record.uid).set(user_data)

        return {
            "uid": user_record.uid,
            "email": user.email,
            "name": user.name,
            "token": custom_token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    try:
        user_record = auth.get_user_by_email(user.email)
        custom_token = auth.create_custom_token(user_record.uid)

        # Fetch user details from Firestore
        user_data = db.collection("users").document(user_record.uid).get().to_dict()

        return {
            "token": custom_token,
            "email": user_data["email"],
            "name": user_data["name"]
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

