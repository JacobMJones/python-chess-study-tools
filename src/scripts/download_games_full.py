import requests
import json
import pandas as pd
import os

def ensure_directory_exists(path):
    """Ensure that the directory exists, and if not, create it."""
    os.makedirs(path, exist_ok=True)

def download_chess_games(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    headers = {"User-Agent": "mrjacobtaiwan@gmail.com"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        archives = response.json().get('archives', [])
        all_games = []
        for archive_url in archives:
            month_games_response = requests.get(archive_url, headers=headers)
            if month_games_response.status_code == 200:
                month_games_data = month_games_response.json()
                all_games.extend(month_games_data.get('games', []))
        
        directory_path = f"C:/Users/Personal/code/chess-tools/src/data/{username}"
        ensure_directory_exists(directory_path)
        json_path = f"{directory_path}/{username}_chess_games.json"
        with open(json_path, "w") as file:
            json.dump(all_games, file)
        
        print(f"Downloaded {len(all_games)} games for user {username}")
        return json_path
    else:
        print(f"Failed to retrieve archives. Status code: {response.status_code}")
        return None

def save_to_excel(df, filename):
    """Save DataFrame to an Excel file."""
    df.to_excel(filename, index=False)
    print(f"Excel file saved successfully to {filename}!")

def save_to_csv(df, filename):
    """Save DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"CSV file saved successfully to {filename}!")

def main(username):
    json_path = download_chess_games(username)
    if json_path:
        df = pd.read_json(json_path)

        # Modify the file names as needed
        directory_path = f"C:/Users/Personal/code/chess-tools/src/data/{username}"
        ensure_directory_exists(directory_path)
        excel_filename = f"{directory_path}/{username}_chess_games.xlsx"
        csv_filename = f"{directory_path}/{username}_chess_games.csv"

        save_to_excel(df, excel_filename)
        save_to_csv(df, csv_filename)

if __name__ == '__main__':
    username = "ADD USERNAME HERE" 
    main(username)
