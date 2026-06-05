from collections import defaultdict

from app.model.assist import Assist
from app.model.blocked_shot import BlockedShot
from app.model.current_players import CurrentPlayers
from app.model.faceoff import Faceoff
from app.model.goalie_change import GoalieChange
from app.model.hit import Hit
from app.model.penalty import Penalty
from app.model.penalty_shot import PenaltyShot
from app.model.player_history import PlayerHistory
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
            "period": g.period,
            "time": format_time(g.time),
            "data": {
                "scorer": g.scorer_id,
                "assists": [
                    {
                        "player": a.player_id,
                        "type": "primary" if a.primary_secondary == 1 else "secondary"
                    }
                    for a in assist_by_goal[g.id]
                ],
                "plus": [
                    {
                        "player": p.player_id
                    } for p in plus_by_goal[g.id]
                ],
                "minus": [
                    {
                        "player": m.player_id
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
                "taken_by": p.taken_by_id,
                "served_by": p.served_by_id,
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
                "shooter": s.shooter_id,
                "goalie": s.goalie_id,
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
                "player": h.player_id,
                "on_player": h.on_player_id if h.on_player_id is not None else None,
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
                "shooter": b.shooter_id,
                "blocker": b.blocker_id,
                "goalie": b.goalie_id,
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
                "home_player": f.home_player_id,
                "visiting_player": f.visiting_player_id,
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
                "goalie": g.player_id,
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
                "shooter": p.shooter_id,
                "goalie": p.goalie_id,
                "goal": p.is_goal
            }
        })

    shootout = {
        "type": "shootout",
        "rounds": {
            round:
            [
                {
                    "shooter": s.shooter_id,
                    "goalie": s.goalie_id,
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
        "home_team_goals": game.home_goals,
        "visiting_team": game.visiting_team.name,
        "visiting_team_goals": game.visiting_goals,
        "win_type": game.win_type,
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

def get_game_summary_json(db, game_id: int):
    game = db.query(Game).filter(Game.id == game_id).first()

    current = db.query(
                    CurrentPlayers.id.label("id"),
                    CurrentPlayers.team_id.label("team_id"),
                    CurrentPlayers.position.label("position"),
                    CurrentPlayers.jersey_number.label("jersey_number")
                ).filter(
                    (CurrentPlayers.team_id == game.visiting_team_id) | (CurrentPlayers.team_id == game.home_team_id)
                )
    previous = db.query(
                    PlayerHistory.id.label("id"),
                    PlayerHistory.team_id.label("team_id"),
                    PlayerHistory.position.label("position"),
                    PlayerHistory.jersey_number.label("jersey_number")
                ).filter(
                    (PlayerHistory.team_id == game.home_team_id) | (PlayerHistory.team_id == game.visiting_team_id), 
                    PlayerHistory.start_date <= game.date,
                    PlayerHistory.end_date >= game.date
                )
    
    roster_subq = current.union_all(previous).subquery()

    roster = (
            db.query(
                Player,
                roster_subq.c.jersey_number,
                roster_subq.c.team_id
            )
            .join(roster_subq, Player.id == roster_subq.c.id)
            .all()
        )
    
    id_by_team = defaultdict(list)
    home = game.home_team_id
    visiting = game.visiting_team_id
    for player, jersey_number, team_id in roster:
        if team_id == home:
            id_by_team[home].append(player.id)
        else:
            id_by_team[visiting].append(player.id)

    
    shots = db.query(Shot).filter(Shot.game_id == game_id).all()
    # print(len(shots))

    home_shots_by_period = defaultdict(list)
    visiting_shots_by_period = defaultdict(list)
    for s in shots:
        # print(s.period, s.shooter_id)
        if s.shooter_id in id_by_team[home]:
            home_shots_by_period[s.period].append(s)
        else:
            visiting_shots_by_period[s.period].append(s)

    # print(home_shots_by_period, visiting_shots_by_period)
    

    pd_list = home_shots_by_period.keys()

    shots_data = {
        pd: {
            "home": len(home_shots_by_period[pd]),
            "visiting": len(visiting_shots_by_period[pd])
        } for pd in pd_list
    } | {
        "total": {
            "home": sum([len(home_shots_by_period[pd]) for pd in pd_list]),
            "visiting": sum([len(visiting_shots_by_period[per]) for per in pd_list]),
        }
    }

    goals = db.query(Goal).filter(Goal.game_id == game_id).all()

    home_goals_by_period = defaultdict(list)
    visiting_goals_by_period = defaultdict(list)

    for g in goals:
        if g.scorer_id in id_by_team[home]:
            home_goals_by_period[g.period].append(g)
        else:
            visiting_goals_by_period[g.period].append(g)

    goals_data = {
        pd: {
            "home": len(home_goals_by_period[pd]) ,
            "visiting": len(visiting_goals_by_period[pd])
        } for pd in pd_list
    } | {
        "total": {
            "home": sum([len(home_goals_by_period[pd]) for pd in pd_list]),
            "visiting": sum([len(visiting_goals_by_period[pd]) for pd in pd_list])
        }
    }

    
    
    penalties = db.query(Penalty).filter(Penalty.game_id == game_id).all()
    
    home_penalties_by_period = defaultdict(list)
    visiting_penalties_by_period = defaultdict(list)

    for p in penalties:
        if p.taken_by_id in id_by_team[home]:
            home_penalties_by_period[p.period].append(p)
        else:
            visiting_penalties_by_period[p.period].append(p)

    penalties_data = {
        pd: {
            "home": len(home_penalties_by_period[pd]),
            "visiting": len(visiting_penalties_by_period[pd])
        } for pd in pd_list
    } | {
        "total": {
            "home": sum([len(home_penalties_by_period[pd]) for pd in pd_list]),
            "visiting": sum([len(visiting_penalties_by_period[pd]) for pd in pd_list])
        }
    }


    game_data = {
        "game_id": game.id,
        "date": str(game.date),
        "home_team": game.home_team.name,
        "home_team_goals": game.home_goals,
        "visiting_team": game.visiting_team.name,
        "visiting_team_goals": game.visiting_goals,
        "win_type": game.win_type,
        "season": game.game_season.name,
        "venue": game.game_venue.name,
        "start_time": game.start_time,
        "end_time": game.end_time,
        "duration": game.duration,
        "attendance": game.attendance,
        "data": {
            "shots": shots_data,
            "goals": goals_data,
            "penalties": penalties_data
        }
    }

    return game_data
