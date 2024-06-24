import pandas as pd
import re

#
player = 'mowbojones'
# Load the CSV data
data = pd.read_csv(f'../data/{player}/{player}_chess_games.csv')

# Extract necessary information and reformat the PGN
def simplify_pgn(pgn):
    lines = pgn.splitlines()
    headers = [line for line in lines if line.startswith("[White ") or line.startswith("[Black ") or line.startswith("[Date ") or line.startswith("[ECO ") or line.startswith("[ECOUrl ")]
    # Extract player names, result, date, ECO, and ECOUrl name
    white = re.search(r'\[White "(.*?)"\]', pgn)
    black = re.search(r'\[Black "(.*?)"\]', pgn)
    white_name = white.group(1) if white else "Unknown"
    black_name = black.group(1) if black else "Unknown"
    date_match = re.search(r'\[Date "(.*?)"\]', pgn)
    date = date_match.group(1) if date_match else "Unknown"
    eco_match = re.search(r'\[ECO "(.*?)"\]', pgn)
    eco = eco_match.group(1) if eco_match else "Unknown"
    eco_url_match = re.search(r'\[ECOUrl "(.*?)"\]', pgn)
    eco_name = eco_url_match.group(1).split('/')[-1] if eco_url_match else "Unknown"
    result_match = re.search(r'\[Result "(.*?)"\]', pgn)
    if result_match:
        result_code = result_match.group(1)
        if result_code == "1-0":
            result = "0"
        elif result_code == "0-1":
            result = "1"
        elif result_code == "1/2-1/2":
            result = "3"
        else:
            result = "3"
    else:
        result = "3"
    # Extract and clean moves
    moves = []
    for line in lines:
        if line and line[0].isdigit():
            clean_line = re.sub(r"\{[^}]*\}", "", line)  # Remove annotations
            clean_line = re.sub(r"\([^)]*\)", "", clean_line)  # Remove variations
            clean_line = re.sub(r"\d+\.", "", clean_line)  # Remove move numbers
            clean_line = re.sub(r"\.\.", "", clean_line)  # Remove dots indicating opponent moves
            clean_line = re.sub(r"\s{2,}", " ", clean_line)  # Remove extra spaces
            moves.append(clean_line.strip())
    simple_moves = " ".join(moves)
    simple_moves = re.sub(r"(1-0|0-1|1/2-1/2)$", "", simple_moves).strip()  # Remove game result from moves
    return "\n".join(headers + [simple_moves]), simple_moves, white_name, black_name, result, date, eco, eco_name

# Apply simplification to each row and separate into new columns
data[['new_pgn', 'moves_pgn', 'white', 'black', 'result', 'date', 'eco', 'eco_name']] = data['pgn'].apply(lambda x: pd.Series(simplify_pgn(x)))

# Keep only the necessary columns
simplified_data = data[['url', 'new_pgn', 'moves_pgn', 'white', 'black', 'result', 'date', 'eco', 'eco_name']]

# Save the simplified data to a new Excel file
simplified_data.to_excel(f'../data/{player}/{player}_organized_games.xlsx', index=False)
