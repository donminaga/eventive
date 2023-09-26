from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import user_routes, event_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/api")
app.include_router(event_routes.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="templates"), name="ui")


@app.get("/")
def read_root():
    return {"message": "Welcome to Eventive!"}
