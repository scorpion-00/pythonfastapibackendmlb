from fastapi import APIRouter
from app.services.team_service import list_all_teams
from app.services.player_service import list_all_players

router = APIRouter()

@router.get("/list_teams")
def list_teams():
    """
    List all teams
    """
    teams = list_all_teams()
    return teams

@router.get("/players/{team_id}")
def list_players(team_id: int):
    """
    List all players for a team
    """
    players = list_all_players(team_id)
    return players

@router.get("/team_and_players")
def list_teams_and_players():
    """
    List all teams and their players in it.
    """
    teams = list_all_teams()
    for team in teams:
        team["players"] = list_all_players(team["id"])
    return teams