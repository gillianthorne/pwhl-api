from fastapi import APIRouter, Depends

from app.database import SessionLocal
from app.services.game_service import build_game_json, get_games_json


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

@router.get("/{game_id}/{event_type}")
def get_event_type(game_id:int, event_type:str, db=Depends(get_db)):
    events =  build_game_json(db, game_id)["events"]

    filtered = [e for e in events if e["type"] == event_type]

    if not filtered:
        return {"error": "no events found or invalid type"}
    
    return filtered
    
@router.get("/")
def get_all_games(
    team_id: int | None = None,
    league_year: str | None = None,
    season_type: int | None = None,
    db = Depends(get_db)
):
    None

    # get query filters
    qf = {}
    qf["team_id"] = team_id if team_id else None
    qf["league_year"] = league_year if league_year else None
    qf["season_type"] = season_type if season_type else None

    return get_games_json(db, qf)
