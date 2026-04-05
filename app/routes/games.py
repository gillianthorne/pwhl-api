from fastapi import APIRouter, Depends

from app.database import SessionLocal
from app.services.game_service import build_game_json


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{game_id}")
def get_game(game_id:int, db=Depends(get_db)):
    return build_game_json(db, game_id)
