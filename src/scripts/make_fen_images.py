import pandas as pd
import ast
import os
import chess
import uuid
from fen_to_image import draw_board

# Step 1: Load and Process Data with Filtering
def process_fen_data_with_filter(file_path, num_moves, threshold=-1):
    data = pd.read_excel(file_path)
    data['index'] = data.index  # Assign the DataFrame index to a new column 'index'
    fields_to_convert = ['moves', 'change', 'best_move']
    for field in fields_to_convert:
        data[field] = data[field].apply(ast.literal_eval)
    data['change'] = data['change'].apply(lambda x: [float(val) for val in x])

    fen_details = {}

    for index, row in data.iterrows():
        board = chess.Board()
        moves = row['moves'][:num_moves] if not isinstance(row['moves'], list) else row['moves'][:num_moves]
        changes = row['change'][:num_moves] if not isinstance(row['change'], list) else row['change'][:num_moves]

        for move_index, (move, change) in enumerate(zip(moves, changes)):
            fen_before_move = board.fen()
            board.push_san(move)

            if change <= threshold:
                if fen_before_move not in fen_details:
                    fen_details[fen_before_move] = {
                        'occurrences': 0,
                        'eco_name': row['eco'],
                        'indexes': set(),
                        'bad_move': move,
                        'good_move': row['best_move'][move_index] if move_index < len(row['best_move']) else '',
                        'image_path': ''
                    }

                fen_details[fen_before_move]['occurrences'] += 1
                fen_details[fen_before_move]['indexes'].add(row['index'])
                break  # Stop after the first significant drop

    return fen_details

# Step 2: Save Images and Update FENs
def save_images_and_update_fens(fen_details, player):
    fens_data = []

    for fen, details in fen_details.items():
        eco_name = details['eco_name'].replace(" ", "_")  # Replace spaces with underscores for file naming
        unique_count = len(details['indexes'])  # Use the number of unique indexes

        # Create the directory path
        directory_path = f'../data/{player}/{player}_chess_positions/{unique_count}-{eco_name}'
        os.makedirs(directory_path, exist_ok=True)

        # Generate a single UUID for both question and answer images
        unique_id = str(uuid.uuid4())
        question_image_filename = f"question-{unique_id}.png"
        answer_image_filename = f"answer-{unique_id}.png"
        question_full_path = f"{directory_path}/{question_image_filename}"
        answer_full_path = f"{directory_path}/{answer_image_filename}"

        # Check if the images already exist before creating new ones
        if not os.path.exists(question_full_path) or not os.path.exists(answer_full_path):
            board_before_move = chess.Board(fen)
            board_image = draw_board(board_before_move, details['good_move'], details['bad_move'])
            blank_board_image = draw_board(board_before_move)
            
            blank_board_image.save(question_full_path)
            board_image.save(answer_full_path)

            print(f"Saved images to {question_full_path} and {answer_full_path}")
        
        details['image_path'] = question_full_path
        fens_data.append({
            'fen': fen,
            'eco_name': details['eco_name'],
            'indexes': '; '.join(map(str, details['indexes'])),
            'bad_move': details['bad_move'],
            'good_move': details['good_move'],
            'image_path': details['image_path']
        })

    # Save the FEN details to fens.xlsx
    fens_df = pd.DataFrame(fens_data)
    fens_df.to_excel(f'../data/{player}/fens.xlsx', index=False)

# Example usage
file_path = '../data/mowbojones/analyzed_games_extended.xlsx'
player = 'mowbojones'
num_moves = 10
threshold = -1
fen_details = process_fen_data_with_filter(file_path, num_moves, threshold)
save_images_and_update_fens(fen_details, player)