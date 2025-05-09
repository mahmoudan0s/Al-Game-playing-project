def get_move(player, board):
    """Gets and validates player move"""
    while True:
        try:
            move = input(f"Player {'X' if player == 1 else 'O'}, enter your move (row,col): ")
            row, col = map(int, move.split(','))

            if 0 <= row < 15 and 0 <= col < 15:
                if board[row][col] == 0:
                    return row, col
                print("Position already occupied!")
            else:
                print("Coordinates must be between 0 and 14")
        except ValueError:
            print("Invalid input. Please enter as: row,col (e.g. 7,7)")
def print_board(board):
    """Prints the Gomoku board with coordinates"""
    size = len(board)
    # Column headers (0-14)
    print("\n    " + " ".join(f"{i:2}" for i in range(size)))

    for i in range(size):
        print(f"{i:2} ", end="")
        for j in range(size):
            if board[i][j] == 0:
                print(" .", end="")
            elif board[i][j] == 1:
                print(" X", end="")
            else:
                print(" O", end="")
        print()

def check_winner(board, row, col, player):
    """Checks if the last move won the game"""
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],  # Vertical
        [(1, 1), (-1, -1)],  # Diagonal \
        [(1, -1), (-1, 1)]  # Diagonal /
    ]

    for dir_pair in directions:
        count = 1
        for dx, dy in dir_pair:
            x, y = row + dx, col + dy
            while 0 <= x < 15 and 0 <= y < 15 and board[x][y] == player:
                count += 1
                x += dx
                y += dy
                if count == 5:
                    return True
    return False


def main():
    print("GOMOKU - Five in a Row")
    print("Enter moves as: row,col (e.g. 7,7 for center)")
    print("Player 1: X, Player 2: O\n")

    board = [[0 for _ in range(15)] for _ in range(15)]
    current_player = 1

    while True:
        print_board(board)
        row, col = get_move(current_player, board)
        board[row][col] = current_player

        if check_winner(board, row, col, current_player):
            print_board(board)
            print(f"\nPlayer {'X' if current_player == 1 else 'O'} wins!")
            break

        current_player = 2 if current_player == 1 else 1


if __name__ == "__main__":
    main()