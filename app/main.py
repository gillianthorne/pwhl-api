from fastapi import FastAPI

from app.routes import games, teams

app = FastAPI()

app.include_router(games.router, prefix="/games")
app.include_router(teams.router, prefix="/teams")