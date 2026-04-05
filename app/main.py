from fastapi import FastAPI

from app.routes import games

app = FastAPI()

app.include_router(games.router, prefix="/games")