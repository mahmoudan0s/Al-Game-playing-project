import math
import random
import time

#Utility Functions
def print_board(board):
    """Prints the Gomoku board with its coordinates"""
    size = len(board)
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

def other_player(player):
    return 2 if player == 1 else 1

def get_move(player, board):
    """Gets and validates player move"""
    while True:
        try:
            move = input(f"Player X, enter your move (row,col): ")
            row, col = map(int, move.split(','))
            if 0 <= row < 15 and 0 <= col < 15:
                if board[row][col] == 0:
                    return row, col
                print("This position already occupied!")
            else:
                print("Enter 2 numbers between 0 and 14")
        except ValueError:
            print("Invalid input. Please enter as: row,col (e.g. 7,7) without parentheses")

def check_winner(board, row=None, col=None, player=None):
    if row is not None and col is not None and player is not None:
        # Check win from specific move
        directions = [[(0, 1), (0, -1)],
                      [(1, 0), (-1, 0)],
                      [(1, 1), (-1, -1)],
                      [(1, -1), (-1, 1)]]
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
    else:
        for i in range(15):
            for j in range(15):
                if board[i][j] != 0:
                    if check_winner(board, i, j, board[i][j]):
                        return True
        return False

#Minimax Algorithm
def is_terminal(state):
    _, board = state
    return check_winner(board) or all(board[i][j] != 0 for i in range(15) for j in range(15))

def utility(state):
    _, board = state
    if check_winner(board, None, None, 2):
        return 1000
    elif check_winner(board, None, None, 1):
        return -1000
    else:
        return evaluate_board(board)

def evaluate_board(board):
    score = 0
    center = [(7, 7), (7, 8), (8, 7), (8, 8)]
    for x, y in center:
        if board[x][y] == 2:
            score += 5

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for i in range(15):
        for j in range(15):
            for dx, dy in directions:
                if 0 <= i + 4 * dx < 15 and 0 <= j + 4 * dy < 15:
                    window = [board[i + k * dx][j + k * dy] for k in range(5)]
                    score += evaluate_window(window, 2)
                    score -= evaluate_window(window, 1)
    return score

def get_possible_moves(board, look_radius=2):
    moves = set()
    for i in range(15):
        for j in range(15):
            if board[i][j] != 0:
                for x in range(max(0, i - look_radius), min(15, i + look_radius + 1)):
                    for y in range(max(0, j - look_radius), min(15, j + look_radius + 1)):
                        if board[x][y] == 0:
                            moves.add((x, y))
    return list(moves) if moves else [(i, j) for i in range(15) for j in range(15) if board[i][j] == 0]

def minimax(state, depth):
    player, board = state

    if is_terminal(state) or depth == 0:
        return None, utility(state)

    best_move = None

    if player == 2:  # AI is MAX
        max_eval = -math.inf
        for row, col in get_possible_moves(board):
            new_board = [r[:] for r in board]
            new_board[row][col] = player
            _, eval = minimax([other_player(player), new_board], depth - 1)
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)
        return best_move, max_eval
    else:  # Human is MIN
        min_eval = math.inf
        for row, col in get_possible_moves(board):
            new_board = [r[:] for r in board]
            new_board[row][col] = player
            _, eval = minimax([other_player(player), new_board], depth - 1)
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
        return best_move, min_eval

def find_best_move(board, depth=3):
    move, _ = minimax([2, board], depth)
    return move if move else random.choice(get_possible_moves(board))

##############################################################################################
def evaluate_window(window, player):
    opponent = 3 - player
    if window.count(player) == 5:
        return 100000  # direct win
    elif window.count(player) == 4 and window.count(0) == 1:
        return 10000   # strong chance to win
    elif window.count(player) == 3 and window.count(0) == 2:
        return 1000
    elif window.count(player) == 2 and window.count(0) == 3:
        return 100
    elif window.count(opponent) == 4 and window.count(0) == 1:
        return -10000  # block opponent
    else:
        return 0


def alphabeta(state, depth, alpha, beta, maximizing_player):
    player, board = state

    if is_terminal(state) or depth == 0:
        return None, utility(state)

    best_move = None

    moves = get_possible_moves(board)

    if maximizing_player:
        max_eval = -math.inf
        for row, col in moves:
            new_board = [r[:] for r in board]
            new_board[row][col] = player
            _, eval = alphabeta([other_player(player), new_board], depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = math.inf
        for row, col in moves:
            new_board = [r[:] for r in board]
            new_board[row][col] = player
            _, eval = alphabeta([other_player(player), new_board], depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move, min_eval

def find_best_move_minimax(board, depth=3):
    move, _ = minimax([2, board], depth)
    return move if move else random.choice(get_possible_moves(board))

def find_best_move_alphabeta(board, depth=3):
    move, _ = alphabeta([1, board], depth, -math.inf, math.inf, False)
    return move if move else random.choice(get_possible_moves(board))

import time

def main():
    print("GOMOKU Game Mode")
    print("1. Human vs AI")
    print("2. AI vs AI")
    
    while True:
        choice = input("Select mode (1 or 2): ")
        if choice in ['1', '2']:
            break
        else:
            print("Invalid input. Please choose 1 or 2.")

    board = [[0 for _ in range(15)] for _ in range(15)]
    current_player = 1  # Player 1 always starts (X)

    if choice == '1':
        print("You are X (1), AI is O (2)")
    else:
        print("AI 1 (Alpha-Beta - X) vs AI 2 (Minimax - O)")

    while True:
        print_board(board)

        if choice == '1':
            if current_player == 1:
                row, col = get_move(current_player, board)  # human move
            else:
                print("AI is thinking....")
                start_time = time.time()
                row, col = find_best_move(board, depth=3)  # aI move (minimax)
                print(f"The AI played at ({row}, {col}) in {time.time() - start_time:.1f}s")
        else:
            print(f"Player {'O' if current_player == 2 else 'X'} thinking...")
            start_time = time.time()
            if current_player == 2:
                row, col = find_best_move_minimax(board, depth=3)
            else:
                row, col = find_best_move_alphabeta(board, depth=3)
            print(f"Played at ({row}, {col}) in {time.time() - start_time:.2f} seconds")

        board[row][col] = current_player

        if check_winner(board, row, col, current_player):
            print_board(board)
            if choice == '1':
                print("\nAI wins!" if current_player == 2 else "\nCongratulations! You win!")
            else:
                print(f"\nAI {'Minimax (O)' if current_player == 2 else 'Alpha-Beta (X)'} wins!")
            break

        if all(board[i][j] != 0 for i in range(15) for j in range(15)):
            print_board(board)
            print("\nIt's a draw!")
            break

        current_player = other_player(current_player)


##############################################################################################


if __name__ == "__main__":
    main()
