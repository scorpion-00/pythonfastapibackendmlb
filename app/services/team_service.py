import statsapi

def list_all_teams():
    """
    List all teams
    """
    teams = statsapi.get('teams', {'sportId': 1})
    formatted_teams = []
    for team in teams['teams']:
        team_info = {
            'id': team['id'],
            'teamName': team['teamName'],
            'abbreviation': team['abbreviation'],
            'locationName': team['locationName'],
            'firstYearOfPlay': team['firstYearOfPlay'],
            'league': team['league']['name'],
            'division': team['division']['name'],
            'active': team['active']
        }
        formatted_teams.append(team_info)
    return formatted_teams