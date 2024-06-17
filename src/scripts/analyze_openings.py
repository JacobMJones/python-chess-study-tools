import pandas as pd
import chess
import chess.engine
import chess.polyglot
import os
import concurrent.futures
from datetime import datetime, timedelta

player = 'dtimer'
# Load the games from the Excel file
df = pd.read_excel(f'../data/{player}/{player}_organized_games.xlsx')
df = df.iloc[::-1]  # Reverse the DataFrame

engine_path = r"C:\Users\Personal\Code\chess-tools\src\stockfish\stockfish-windows-x86-64.exe"
absolute_engine_path = os.path.abspath(engine_path)
if not os.path.exists(engine_path):
    raise FileNotFoundError(f"The specified engine path does not exist: {engine_path}")

#book_path = "opening/BIN/Perfect2023.bin"
book_path = r"C:\Users\Personal\Code\chess-tools\src\opening_book\OPTIMUS2403.bin"

def analyze_game(data):
    
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
  
    # engine.configure({"Threads": 10})  # Example setting, adjust based on your CPU cores, or dont 
    # engine.configure({"Hash": 2048}) 
    book_reader = chess.polyglot.open_reader(book_path)
    
    moves_pgn, eco, white, black, eco_name = data['moves_pgn'], data['eco'], data['white'], data['black'], data['eco_name']
    board = chess.Board()

    results = {
        'eco': eco,
        'white': white,
        'black': black,
        'eco_name': eco_name,
        'moves': [],
        'book_move': [],
        'suggested_book_move': [],
        'eval_before_move': [],
        'eval_after_move': [],
        'change': [],
        'best_move': [],
        'opponents_best_move': [],
        'best_continuations': [],
    }
    print('in ansss')
    try:
        for move in moves_pgn.split():
            eval_before_move = get_current_evaluation(board, engine)
            best_move, _ = get_best_move_and_evaluation(board, engine)
            board.push_san(move)
            eval_after_move = get_current_evaluation(board, engine)
            difference = round(eval_after_move - eval_before_move, 2)
            top_book_move, in_book = move_in_opening_book(board, book_reader)
            opponents_best_move, continuation = get_best_move_and_evaluation(board, engine)
            results['moves'].append(move)
            results['book_move'].append(in_book)
            results['suggested_book_move'].append(str(top_book_move))
            results['eval_before_move'].append(str(eval_before_move))
            results['eval_after_move'].append(str(eval_after_move))
            results['change'].append(str(difference))
            results['best_move'].append(best_move)
            results['opponents_best_move'].append(opponents_best_move)
            results['best_continuations'].append(' '.join(continuation))
       
    finally:
        print(f"Game analyzed: {eco} between {white} and {black}")
        engine.quit()
        book_reader.close()

    return results

def get_current_evaluation(board, engine):
    info = engine.analyse(board, chess.engine.Limit(time=2, depth=25))
    return format_eval(info['score'], board)

def get_best_move_and_evaluation(board, engine):
    info = engine.analyse(board, chess.engine.Limit(time=2, depth=25), multipv=3)
    if isinstance(info, list) and len(info) > 0:
        continuation = []
        for item in info:
            if 'pv' in item:  # Check if 'pv' key exists
                sequence = [board.san(move) for move in item['pv'] if move in board.legal_moves]
                if sequence:
                    continuation.extend(sequence)
        best_move = continuation[0] if continuation else "Illegal move"
        return best_move, continuation
    return "No move available", []

def move_in_opening_book(board, book_reader):
    try:
        entry = book_reader.find(board)
        return board.san(entry.move), "Yes"  # Convert UCI to SAN here
    except IndexError:
        return None, "No"

def format_eval(score, board):
    eval_score = score.relative.score(mate_score=10000) / 100
    return eval_score if board.turn == chess.WHITE else -eval_score

def save_results_to_excel(results):
    df_results = pd.DataFrame(results)
    file_path = f'../data/{player}/{player}_analyzed_games_extended.xlsx'
    
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and write the data
        df_results.to_excel(file_path, index=False)
    else:
        # If the file exists, read the existing data and append the new data
        existing_df = pd.read_excel(file_path)
        combined_df = pd.concat([existing_df, df_results], ignore_index=True)
        combined_df.to_excel(file_path, index=False)
    
    print("Results saved to Excel.")

if __name__ == "__main__":
    
    #Games to analyze before saving
    BATCH_SIZE = 10


    #Filter what you analyze
    
    #restrict analysis by ECO
    df = df[df['eco'].str.startswith('D')]
    
    # Filter the DataFrame to include only the last 6 months
    df = df[df['date'] > datetime.now() - timedelta(days=6*30)]
    
    total_games = len(df)

    start_batch = 0 # Set this to the batch number you want to start from

    for i in range(start_batch * BATCH_SIZE, total_games, BATCH_SIZE):
        print(f"Processing batch {i//BATCH_SIZE + 1}/{(total_games + BATCH_SIZE - 1) // BATCH_SIZE}")
        batch_data = df.iloc[i:i + BATCH_SIZE].to_dict(orient='records')
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(analyze_game, batch_data))
        save_results_to_excel(results)
        print(f"Batch {i//BATCH_SIZE + 1} completed.")
