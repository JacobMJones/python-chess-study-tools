import chess
from PIL import Image, ImageDraw, ImageFont


def draw_board(board, best_move=None, your_move=None, square_size=60):
    colors = [(235, 236, 208), (115, 149, 82)]
    pieces_images = {
        'r': '../images/pieces/black_rook.png',
        'n': '../images/pieces/black_knight.png',
        'b': '../images/pieces/black_bishop.png',
        'q': '../images/pieces/black_queen.png',
        'k': '../images/pieces/black_king.png',
        'p': '../images/pieces/black_pawn.png',
        'R': '../images/pieces/white_rook.png',
        'N': '../images/pieces/white_knight.png',
        'B': '../images/pieces/white_bishop.png',
        'Q': '../images/pieces/white_queen.png',
        'K': '../images/pieces/white_king.png',
        'P': '../images/pieces/white_pawn.png'
    }
    board_image = Image.new('RGB', (square_size * 8, square_size * 8 + 60 if best_move or your_move else square_size * 8), (245, 255, 255))
    draw = ImageDraw.Draw(board_image)
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            draw.rectangle([col * square_size, row * square_size, (col + 1) * square_size, (row + 1) * square_size], fill=color)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = Image.open(pieces_images[piece.symbol()])
            piece_image = piece_image.resize((square_size, square_size), Image.ANTIALIAS)
            x = chess.square_file(square) * square_size
            y = (7 - chess.square_rank(square)) * square_size
            board_image.paste(piece_image, (x, y), piece_image)
    if best_move or your_move:
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font = ImageFont.load_default()
        if best_move:
            draw.text((10, square_size * 8 + 5), f"Best Move: {best_move}", (0, 0, 0), font=font)
        if your_move:
            draw.text((10, square_size * 8 + 25), f"Your Move: {your_move}", (0, 0, 0), font=font)
    return board_image
