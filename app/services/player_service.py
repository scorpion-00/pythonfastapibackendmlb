import statsapi
from typing import List, Dict

def get_player_image_url(player_id: int) -> str:
    """
    Generate the MLB headshot image URL for a player
    """
    return f"https://content.mlb.com/images/headshots/current/60x60/{player_id}@2x.png"

def list_all_players(team_id: int) -> List[Dict]:
    """
    List all players for a team including their headshot image URLs
    
    Args:
        team_id (int): MLB team ID
        
    Returns:
        List[Dict]: List of player information dictionaries
    """
    players = statsapi.get('team_roster', {'teamId': team_id})
    formatted_players = []
    
    for player in players['roster']:
        player_id = player['person']['id']
        player_info = {
            'id': player_id,
            'fullName': player['person']['fullName'],
            'jerseyNumber': player['jerseyNumber'],
            'position': player['position']['name'],
            'imageUrl': get_player_image_url(player_id)
        }
        formatted_players.append(player_info)
    
    return formatted_players