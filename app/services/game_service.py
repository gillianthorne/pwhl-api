from collections import defaultdict

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


def build_game_json(db, game_id: int):
    game = db.query(Game).filter(Game.id == game_id).first()

    goals = db.query(Goal).filter(Goal.game_id == game_id).all()

    assists = db.query(Assist).join(Goal).filter(Goal.game_id == game_id).all()
    assist_by_goal = defaultdict(list)
    for a in assists:
        assist_by_goal[a.goal_id].append(a)

    plusminus = db.query(PlusMinus).join(Goal).filter(Goal.game_id == game_id).all()
    plus_by_goal = defaultdict(list)
    minus_by_goal = defaultdict(list)
    for pm in plusminus:
        plus_by_goal[pm.goal_id].append(pm) if pm.is_plus else minus_by_goal[pm.goal_id].append(pm)

    penalties = db.query(Penalty).filter(Penalty.game_id == game_id).all()

    shots = db.query(Shot).filter(Shot.game_id == game_id).all()

    hits = db.query(Hit).filter(Hit.game_id == game_id).all()

    blocked_shots = db.query(BlockedShot).filter(BlockedShot.game_id == game_id).all()

    faceoffs = db.query(Faceoff).filter(Faceoff.game_id == game_id).all()

    goalie_changes = db.query(GoalieChange).filter(GoalieChange.game_id == game_id).all()

    penalty_shots = db.query(PenaltyShot).filter(PenaltyShot.game_id == game_id).all()

    shootouts = db.query(Shootout).filter(Shootout.game_id == game_id).all()
    shootouts_by_round = defaultdict(list)
    for s in shootouts:
        shootouts_by_round[s.shootout_attempt].append(s)
    print(shootouts_by_round)

    goal_list = []
    for g in goals:
        goal_list.append({
            "type": "goal",
            "id": g.id,
            "scorer_id": g.scorer.id,
            "scorer": g.scorer.name,
            "period": g.period,
            "time": str(g.time),
            "data": {
                "assists": [
                    {
                        "player_id": a.player.id,
                        "player": a.player.name,
                        "type": "primary" if a.primary_secondary == 1 else "secondary"
                    }
                    for a in assist_by_goal[g.id]
                ],
                "plus": [
                    {
                        "player_id": p.player.id,
                        "player": p.player.name
                    } for p in plus_by_goal[g.id]
                ],
                "minus": [
                    {
                        "player_id": m.player.id,
                        "player": m.player.name
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
            "time": str(p.time),
            "data": {
                "taken_by_id": p.taken_by.id,
                "taken_by": p.taken_by.name,
                "served_by_id": p.served_by.id,
                "served_by": p.served_by.name,
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
            "time": str(s.time),
            "data": ({
                "shooter_id": s.shooter.id,
                "shooter": s.shooter.name,
                "goalie_id": s.goalie.id,
                "goalie": s.goalie.name,
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
            "time": str(h.time),
            "data": {
                "player_id": h.player.id,
                "player": h.player.name,
                "on_player_id": h.on_player.id if h.on_player is not None else None,
                "on_player": h.on_player.name if h.on_player is not None else None,
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
            "time": str(b.time),
            "data": {
                "shooter_id": b.shooter.id,
                "shooter": b.shooter.name,
                "blocker_id": b.shooter.id,
                "blocker": b.blocker.name,
                "goalie_id": b.goalie.id,
                "goalie": b.goalie.name,
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
            "time": str(f.time),
            "data": {
                "home_player_id": f.home_player.id,
                "home_player": f.home_player.name,
                "visiting_player_id": f.visiting_player.id,
                "visiting_player": f.visiting_player.name,
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
            "time": str(g.time),
            "data": {
                "goalie_id": g.player.id,
                "goalie": g.player.name,
                "entering": g.entering
            }
        })

    penalty_shot_list = []
    for p in penalty_shots:
        penalty_shot_list.append({
            "type": "penalty_shot",
            "id": p.id,
            "period": p.period,
            "time": str(p.time),
            "data": {
                "shooter_id": p.shooter.id,
                "shooter": p.shooter,
                "goalie_id": p.goalie.id,
                "goalie": p.goalie,
                "goal": p.is_goal
            }
        })

    shootout = {
        "type": "shootout",
        "rounds": {
            round:
            [
                {
                    "shooter_id": s.shooter.id,
                    "shooter": s.shooter.name,
                    "goalie_id": s.goalie.id,
                    "goalie": s.goalie.name,
                    "goal": s.is_goal,
                    "gamewinninggoal": s.is_gamewinninggoal
                }
            for s in shootouts_by_round[round]
            ]
            
        for round in range(1, len(shootouts_by_round)+1)
        }
    }
    return {
        "game_id": game.id,
        "date": str(game.date),
        "goals": goal_list,
        "penalties": penalty_list,
        "shots": shot_list,
        "hits": hit_list,
        "blocked_shots": blocked_shot_list,
        "faceoffs": faceoff_list,
        "goalie_changes": goalie_change_list,
        "penalty_shots": penalty_shot_list,
        "shootout": shootout,
    }