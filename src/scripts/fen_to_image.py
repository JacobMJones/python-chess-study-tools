import chess
import chess.pgn
from PIL import Image, ImageDraw

def draw_board(board, square_size=60):
    colors = [(240, 217, 181), (181, 136, 99)]
    pieces_images = {
        'r': 'images/pieces/black_rook.png',
        'n': 'images/pieces/black_knight.png',
        'b': 'images/pieces/black_bishop.png',
        'q': 'images/pieces/black_queen.png',
        'k': 'images/pieces/black_king.png',
        'p': 'images/pieces/black_pawn.png',
        'R': 'images/pieces/white_rook.png',
        'N': 'images/pieces/white_knight.png',
        'B': 'images/pieces/white_bishop.png',
        'Q': 'images/pieces/white_queen.png',
        'K': 'images/pieces/white_king.png',
        'P': 'images/pieces/white_pawn.png'
    }

    # Create a new image with white background
    board_image = Image.new('RGB', (square_size * 8, square_size * 8), (255, 255, 255))
    draw = ImageDraw.Draw(board_image)

    # Draw squares
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            draw.rectangle([col * square_size, row * square_size, 
                            (col + 1) * square_size, (row + 1) * square_size], fill=color)

    # Draw pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = Image.open(pieces_images[piece.symbol()])
            piece_image = piece_image.resize((square_size, square_size), Image.ANTIALIAS)
            x = chess.square_file(square) * square_size
            y = (7 - chess.square_rank(square)) * square_size
            board_image.paste(piece_image, (x, y), piece_image)

    return board_image

# Load from FEN
fen = "r1bqkbnr/pppp1ppp/4n3/1P2p3/8/4P3/PBPP1PPP/RN1QKBNR w KQkq - 1 5"
board = chess.Board(fen)

# Draw board and save as image
image = draw_board(board)
image.save("chess_board.png")
