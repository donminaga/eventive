# utils/firebase.py

import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("../../firebase_credentials.json")  # Adjust the path accordingly
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user(email: str):
    users = db.collection("users").where("email", "==", email).stream()
    user_list = list(users)
    if user_list:
        return user_list[0]
    return None

# ... any other Firebase related helper functions ...
