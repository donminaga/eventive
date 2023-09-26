# Eventive

Plan ahead, stay ahead.

Eventive is a web-based event planner application that allows users to create events, send invitations, and manage RSVPs. It's built using FastAPI and integrates with Firebase for user authentication and data storage.

## Features:
- **User Registration and Login**: Secure registration and login using Firebase authentication.
- **Event Management**: Users can create, list, and manage their events.
- **Invitations**: Event creators can invite other users via email.
- **RSVP**: Invited users can RSVP to events to indicate their attendance status.

## Getting Started:
1. Clone the repository.
2. Set up a virtual environment:
    ```commandline
    python -m venv venv 
    source venv/bin/activate
    ```
   or, for windows
   ```commandline
   venv\Scripts\activate
   ```
3. Install the required dependencies
   ```commandline
   pip install -r requirements.txt
   ```
4. Set up Firebase and download the service account key
   - Rename it to `firebase-credentials.json` and place it in the root directory.
5. Run the FastAPI application:
    ```commandline
    uvicorn app.main:app --reload
    ```

## LICENSE
All my code is MIT licensed. Videos and libraries follow their respective licenses.

Contributions, feedback, and improvements are always welcome!