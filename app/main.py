from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import credentials
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/ui", StaticFiles(directory="templates/ui"), name="ui")
firebase_admin.initialize_app(cred)

from .routes import user_routes, event_routes

app.include_router(user_routes.router)
app.include_router(event_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Eventive!"}
