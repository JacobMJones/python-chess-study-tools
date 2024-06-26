import requests
import json 
def download_chess_games(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    headers = {
        "User-Agent": "ADD EMAIL ADDRESS HERE"  
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        archives = response.json().get('archives', [])
        all_games = []

        for archive_url in archives:
            month_games_response = requests.get(archive_url, headers=headers)
            month_games_data = month_games_response.json()
            all_games.extend(month_games_data.get('games', []))
        with open(f"../data/{username}/{username}_chess_games.json", "w") as file:
            json.dump(all_games, file)
        
        print(f"Downloaded {len(all_games)} games for user {username}")
    else:
        print(f"Failed to retrieve archives. Status code: {response.status_code}")

download_chess_games("ADD USERNAME HERE")