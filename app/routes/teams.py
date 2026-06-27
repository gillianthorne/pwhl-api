from fastapi import APIRouter, Depends

from app.database import SessionLocal
from app.services.teams_service import build_roster, build_teams_json


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

@router.get("/")
def get_teams(db=Depends(get_db)):
    return build_teams_json(db)

@router.get("/{team_id}/roster")
def get_team_roster(
    team_id,
    season: str | None = None,
    db = Depends(get_db)
):
    return build_roster(db, team_id, season)