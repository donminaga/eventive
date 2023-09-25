from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
import os

# Get the absolute path to the directory containing main.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use os.path.join to get the path to firebase-credentials.json
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')

cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)


app = FastAPI()

firebase_admin.initialize_app(cred)

from .routes import user_routes, event_routes

app.include_router(user_routes.router)
app.include_router(event_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Eventive!"}
