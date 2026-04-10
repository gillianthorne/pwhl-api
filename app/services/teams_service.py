import datetime
import traceback

from app.model.current_players import CurrentPlayers
from app.model.game import Game
from app.model.goal import Goal
from app.model.player import Player
from app.model.player_history import PlayerHistory
from app.model.season import Season
from app.model.team import Team


def build_teams_json(db):
    # there's a placeholder team -1 so this gets all real teams
    all_teams = db.query(Team).filter(Team.id > 0).all()

    teams = []

    for team in all_teams:
        season = f"{team.first_season.season_year[:4]}-{team.first_season.season_year[6:]}" if team.first_season.season_year[:4] != "0000" else team.first_season.season_year[4:]
        print(season)
        teams.append({
            "id": team.id,
            "name": team.name,
            "abbreviation": team.abbreviation,
            "division": team.division_id,
            "first_season": season
        })


    return teams

def build_roster(db, team_id: int, season: int):

    # we need an actual season object so we can check for any players that previously were on a team if we are looking at the current roster
    # for example jessie eldridge should show up for the seattle torrent even though she is currently a boston fleet
    if season:
        year = db.query(Season).filter(Season.id == season).first().season_year
        print("season yes")
    else:
        year = db.query(Season).filter(Season.start_date <= datetime.datetime.now()).filter(datetime.datetime.now() <= Season.end_date).first().season_year
        print("season no")

    if year == "00002024":
        start = datetime.date(2023, 11, 1)
        end = datetime.date(2024, 6, 1)
    else:
        start = datetime.date(int(year[:4]), 11, 1)
        end = datetime.date(int(year[4:]), 6, 1)

    print(start, end)

    

    try:
        current = db.query(
                        CurrentPlayers.id.label("id"),
                        CurrentPlayers.team_id.label("team_id"),
                        CurrentPlayers.jersey_number.label("jersey_number"),
                        CurrentPlayers.position.label("position")
                    ).filter(
                        CurrentPlayers.team_id == team_id,
                        CurrentPlayers.start_date <= end
                    )
        previous = db.query(
                        PlayerHistory.id.label("id"),
                        PlayerHistory.team_id.label("team_id"),
                        PlayerHistory.jersey_number.label("jersey_number"),
                        PlayerHistory.position.label("position")
                    ).filter(
                        PlayerHistory.team_id == team_id, 
                        PlayerHistory.start_date <= end,
                        PlayerHistory.end_date >= start
                    )


        roster_subq = current.union_all(previous).subquery()

        roster = (
            db.query(
                Player,
                roster_subq.c.jersey_number,
                roster_subq.c.position
            )
            .join(roster_subq, Player.id == roster_subq.c.id)
            .all()
        )
    # print(roster)

        players = []
        for player, jersey_number, position in roster:
            plays_key = "catches" if position == "G" else "shoots"
            plays = player.catches if position == "G" else player.shoots

            players.append({
                "id": player.id,
                "name": player.name,
                "jersey_number": jersey_number,
                "position": position,
                plays_key: plays,
                "date_of_birth": player.birthdate,
                "hometown": player.hometown
            })
        return players
    
    except Exception as e:
        print(e)
        return {"error": "something happened"}
        

def build_team_stats(db, team_id: int, season: int):
    pass