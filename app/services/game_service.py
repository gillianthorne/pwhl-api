from collections import defaultdict

from sqlalchemy.orm import joinedload

from app.model.assist import Assist
from app.model.blocked_shot import BlockedShot
from app.model.faceoff import Faceoff
from app.model.goalie_change import GoalieChange
from app.model.hit import Hit
from app.model.penalty import Penalty
from app.model.penalty_shot import PenaltyShot
from app.model.plus_minus import PlusMinus
from app.model.shootout import Shootout
from app.model.shot import Shot
from app.model.venue import Venue
from app.model.team import Team
from app.model.season_description import SeasonDescription
from app.model.season import Season
from app.model.player import Player
from app.model.game import Game
from app.model.goal import Goal
from utils.utils import time_convert, time_to_seconds, format_time

def build_game_json(db, game_id: int):
    game = db.query(Game).filter(Game.id == game_id).first()

    players = db.query(Player.id, Player.name).all()
    player_map = {p.id: p.name for p in players}

    goals = (
        db.query(Goal)
        .filter(Goal.game_id == game_id)
        .all()
    )
    
    assists = (
        db.query(Assist)
        .join(Goal).
        filter(Goal.game_id == game_id)
        .all()
    )
    assist_by_goal = defaultdict(list)
    for a in assists:
        assist_by_goal[a.goal_id].append(a)

    plusminus = (
        db.query(PlusMinus)
        .join(Goal)
        .filter(Goal.game_id == game_id)
        .all()
    )
    plus_by_goal = defaultdict(list)
    minus_by_goal = defaultdict(list)
    for pm in plusminus:
        plus_by_goal[pm.goal_id].append(pm) if pm.is_plus else minus_by_goal[pm.goal_id].append(pm)

    penalties = (
        db.query(Penalty)
        .filter(Penalty.game_id == game_id)
        .all()
    )

    shots = (
        db.query(Shot)
        .filter(Shot.game_id == game_id)
        .all()
    )

    hits = (
        db.query(Hit)
        .filter(Hit.game_id == game_id)
        .all()
    )

    blocked_shots = (
        db.query(BlockedShot)
        .filter(BlockedShot.game_id == game_id)
        .all()
    )

    faceoffs = (
        db.query(Faceoff)
        .filter(Faceoff.game_id == game_id)
        .all()
    )

    goalie_changes = (
        db.query(GoalieChange)
        .filter(GoalieChange.game_id == game_id)
    )

    penalty_shots = (
        db.query(PenaltyShot)
        .filter(PenaltyShot.game_id == game_id)
        .all()
    )
    
    shootouts = (
        db.query(Shootout)
        .filter(Shootout.game_id == game_id)
        .all()
    )
    shootouts_by_round = defaultdict(list)
    for s in shootouts:
        shootouts_by_round[s.shootout_attempt].append(s)

    goal_list = []
    for g in goals:
        goal_list.append({
            "type": "goal",
            "id": g.id,
            "scorer": player_map.get(g.scorer_id),
            "period": g.period,
            "time": format_time(g.time),
            "data": {
                "assists": [
                    {
                        "player": player_map.get(a.player_id),
                        "type": "primary" if a.primary_secondary == 1 else "secondary"
                    }
                    for a in assist_by_goal[g.id]
                ],
                "plus": [
                    {
                        "player": player_map.get(p.player_id)
                    } for p in plus_by_goal[g.id]
                ],
                "minus": [
                    {
                        "player": player_map.get(m.player_id)
                    } for m in minus_by_goal[g.id]
                ],
                "strength": {
                    "powerplay": g.is_powerplay,
                    "shorthanded": g.is_shorthanded,
                    "emptynet": g.is_emptynet,
                    "insurance": g.is_insurancegoal,
                    "gamewinning": g.is_gamewinninggoal
                },
                "coordinates" : {
                    "x_location": g.x_location,
                    "y_location": g.y_location
                },
            }            
        })
    
    penalty_list = []
    for p in penalties:
        penalty_list.append({
            "type": "penalty",
            "id": p.penalty_id,
            "period": p.period,
            "time": format_time(p.time),
            "data": {
                "taken_by": player_map.get(p.taken_by_id),
                "seved_by": player_map.get(p.served_by_id),
                "length": p.length,
                "type": p.description,
                "bench": p.is_bench,
                "powerplay": p.is_powerplay
            }
        })

    shot_list = []
    for s in shots: 
        shot_list.append({
            "type": "shot",
            "id": s.id,
            "period": s.period,
            "time": format_time(s.time),
            "data": ({
                "shooter": player_map.get(s.shooter_id),
                "goalie": player_map.get(s.goalie_id),
                "goal": s.is_goal,
                "type": s.type,
                "quality": s.quality,
                "coordinates": {
                    "x_location": s.x_location,
                    "y_location": s.y_location
                }
            })
        })
    
    hit_list = []
    for h in hits:
        hit_list.append({
            "type": "hit",
            "id": h.id,
            "period": h.period,
            "time": format_time(h.time),
            "data": {
                "player": player_map.get(h.player_id),
                "on_player": player_map.get(h.on_player_id) if h.on_player_id is not None else None,
                "coordinates": {
                    "x_location": h.x_location,
                    "y_location": h.y_location
                }
            }
        })
    
    blocked_shot_list = []
    for b in blocked_shots:
        blocked_shot_list.append({
            "type": "blocked_shot",
            "id": b.id,
            "period": b.period,
            "time": format_time(b.time),
            "data": {
                "shooter": player_map.get(b.shooter_id),
                "blocker": player_map.get(b.blocker_id),
                "goalie": player_map.get(b.goalie_id),
                "type": b.type,
                "quality": b.quality,
                "coordinates": {
                    "x_location": b.x_location,
                    "y_location": b.y_location
                },
            }
        })

    faceoff_list = []
    for f in faceoffs:
        faceoff_list.append({
            "type": "faceoff",
            "id": f.id,
            "period": f.period,
            "time": format_time(f.time),
            "data": {
                "home_player": player_map.get(f.home_player_id),
                "visiting_player": player_map.get(f.visiting_player_id),
                "home_win": f.home_win,
                "coordinates": {
                    "x_location": f.x_location,
                    "y_location": f.y_location
                }
            }
        })

    goalie_change_list = []
    for g in goalie_changes:
        goalie_change_list.append({
            "type": "goalie_change",
            "id": g.id,
            "period": g.period,
            "time": format_time(g.time),
            "data": {
                "goalie": player_map.get(g.player_id),
                "entering": g.entering
            }
        })

    penalty_shot_list = []
    for p in penalty_shots:
        penalty_shot_list.append({
            "type": "penalty_shot",
            "id": p.id,
            "period": p.period,
            "time": format_time(p.time),
            "data": {
                "shooter": player_map.get(p.shooter_id),
                "goalie": player_map.get(p.goalie_id),
                "goal": p.is_goal
            }
        })

    shootout = {
        "type": "shootout",
        "rounds": {
            round:
            [
                {
                    "shooter": player_map.get(s.shooter_id),
                    "goalie": player_map.get(s.goalie_id),
                    "goal": s.is_goal,
                    "gamewinninggoal": s.is_gamewinninggoal
                }
            for s in shootouts_by_round[round]
            ]
            
        for round in range(1, len(shootouts_by_round)+1)
        }
    }
    
    timeline = (
        goalie_change_list +
        faceoff_list +
        shot_list +
        goal_list +
        penalty_list +
        hit_list + 
        blocked_shot_list +
        penalty_shot_list
    )

    timeline.sort(
        key= lambda e: (
            e["period"],
            time_to_seconds(e["time"])
        )
    )

    game_data = {
        "game_id": game.id,
        "date": str(game.date),
        "home_team": game.home_team.name,
        "visiting_team": game.visiting_team.name,
        "season": game.game_season.name,
        "venue": game.game_venue.name,
        "attendance": game.attendance
    }

    if len(shootout["rounds"]) > 0:
        return {
            "game_data": game_data,
            "events": timeline,
            "shootout": shootout
        }
    else:
        return {
            "game_data": game_data,
            "events": timeline
        }
    
def get_games_json(db, query_filters: dict):
    query = db.query(Game)

    if query_filters["team_id"]:
        query = query.filter(
            (Game.home_team_id == query_filters["team_id"])
            |
            (Game.visiting_team_id == query_filters["team_id"])
        )

    if query_filters["league_year"]:
        query = query.filter(
            Game.game_season.has(Season.season_year == query_filters["league_year"])
        )

    if query_filters["season_type"]:
        query = query.filter(
            Game.game_season.has(Season.season_type == query_filters["season_type"])
        )

    all_games = query.all()

    games = []
    for game in all_games:
        games.append({
            "id": game.id,
            "date": str(game.date),
            "home_team": game.home_team.name,
            "visiting_team": game.visiting_team.name,
            "season": game.game_season.name,
            "venue": game.game_venue.name,
            "start_time": time_convert(game.start_time),
            "end_time": time_convert(game.end_time),
            "duration": time_convert(game.duration)
        })

    return games