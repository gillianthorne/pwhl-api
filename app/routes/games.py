from fastapi import APIRouter, Depends

from app.database import SessionLocal
from app.services.game_service import build_game_json, get_game_summary_json, get_games_json, get_goalie_stats_json, get_skater_stats_json


router = APIRouter()

def extract_player_ids(event: dict):
    data = event.get("data", {})
    event_type = event.get("type")

    if event_type == "goalie_change":
        return {data["goalie"]}
    
    if event_type == "faceoff":
        return {data["home_player"], data["visiting_player"]}

    if event_type == "goal":
        ids = set()
        if data.get("scorer"):
            ids.add(data["scorer"])
        for a in data.get("assists", []):
            ids.add(a["player"])
        for p in data.get("plus", []):
            ids.add(p["player"])
        for m in data.get("minus", []):
            ids.add(m["player"])
        return ids
    
    if event_type == "shot":
        return {data["shooter"], data["goalie"]}
    
    if event_type == "blocked_shot":
        return {data["shooter"], data["blocker"], data["goalie"]}

    if event_type == "hit":
        return {data["player"], data["on_player"]}
    
    if event_type == "penalty":
        return {data["taken_by"], data["served_by"]}
    
    if event_type == "penalty_shot":
        return {data["shooter"], data["goalie"]}
    
    if event_type == "shootout":
        return {data["shooter"], data["goalie"]}
    
    return set()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@router.get("/{game_id}")
def get_game(
    game_id,
    event_type: str | None = None,
    player_id: int | None = None,
    db = Depends(get_db),
):
    events = build_game_json(db, game_id)
    if not event_type and not player_id:
        print("not event type")
        return events
    
    filtered = events["events"]
    
    if event_type:
        filtered = [e for e in filtered if e["type"] == event_type]
    
    if player_id:
        filtered = [e for e in filtered if player_id in extract_player_ids(e)]

    if not filtered:
        return {"error": "no events found matching the given filters."}

    return filtered  


@router.get("/")
def get_all_games(
    home: int | None = None,
    team_1: int | None = None,
    team_2: int | None = None,
    league_year: str | None = None,
    season_type: int | None = None,
    venue: int | None = None,
    win_type: str | None = None,
    takeover: bool | None = None,
    db = Depends(get_db)
):

    # get query filters
    qf = {}
    qf["home"] = home if home else None
    qf["team_1"] = team_1 if team_1 else None
    qf["team_2"] = team_2 if team_2 else None
    qf["league_year"] = league_year if league_year else None
    qf["season_type"] = season_type if season_type else None
    qf["venue"] = venue if venue else None
    qf["win_type"] = win_type if win_type else None
    qf["takeover"] = takeover if takeover is not None else None

    return get_games_json(db, qf)

@router.get("/{game_id}/summary")
def get_game_summary(
    game_id,
    db = Depends(get_db)
):
    return get_game_summary_json(db, game_id)

@router.get("/{game_id}/stats/skaters")
def get_skater_stats(
    game_id,
    team: int | None = None,
    db = Depends(get_db)
):
    return get_skater_stats_json(db, game_id, team)

@router.get("/{game_id}/stats/goalies")
def get_goalie_stats(
    game_id,
    team: int | None = None,
    db = Depends(get_db)
):
    return get_goalie_stats_json(db, game_id, team)