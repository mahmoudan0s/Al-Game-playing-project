import tkinter as tk
from tkinter import messagebox
import time
from minimaxGomoku import (
    other_player, check_winner, find_best_move_minimax,
    find_best_move_alphabeta, get_possible_moves
)

BOARD_SIZE = 15
CELL_SIZE = 30

# AI 1  (Alpha-Beta - X) = black "play first"
# AI 2 (Minimax - O)  = white    
class GomokuGUI:

    def show_welcome_msg(self):
        welcome_window = tk.Toplevel()
        welcome_window.title("Welcome")
        welcome_window.geometry("300x200")
        welcome_window.grab_set()  # prevent the user to play until he choose the mode

        tk.Label(welcome_window, text="Welcome To Gomoku 🌟", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(welcome_window, text="Please Choose The Game Mode", font=("Helvetica", 12)).pack(pady=5)

        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#f0ad4e", "fg": "white",
            "padx": 10, "pady": 5,
            "bd": 0,
            "activebackground": "#ec971f"
        }
        
        mode_frame = tk.Frame(welcome_window)
        mode_frame.pack(pady=10)

        tk.Button(mode_frame, text="AI vs AI", command=lambda: self.select_mode('ai_vs_ai', welcome_window), **button_style).pack(side=tk.LEFT, padx=10)
        tk.Button(mode_frame, text="User vs AI", command=lambda: self.select_mode('user_vs_ai', welcome_window), **button_style).pack(side=tk.LEFT, padx=10)


    def select_mode(self, mode, window):
        self.game_mode = mode
        window.destroy()
        if mode == "ai_vs_ai":
            self.start_ai_vs_ai()
        else:
            self.start_user_vs_ai()

    def reset_game(self):
        self.status_label.config(text="")  
        self.reset_board()
        if self.game_mode == "ai_vs_ai":
            self.root.after(100, self.ai_vs_ai_turn)

            
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku Game")

        self.turn_label = tk.Label(root, text="Black Turn", font=("Arial", 14))
        self.turn_label.pack()

        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE, bg="burlywood")
        self.canvas.pack()

        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1  # Start with Player 1 (Black)
        self.game_mode = None

        self.show_welcome_msg()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.human_move)

        self.mode_frame = tk.Frame(root)
        self.mode_frame.pack()


        # options frame
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack()

        self.status_label = tk.Label(self.bottom_frame, text="", font=("Arial", 12), fg="green")
        self.status_label.pack()

        self.control_frame = tk.Frame(self.bottom_frame)
        self.control_frame.pack(pady=5)

        control_style = {"font": ("Helvetica", 11, "bold"), "bg": "#5bc0de", "fg": "white", "padx": 10, "pady": 4, "bd": 0, "activebackground": "#31b0d5"}
        tk.Button(self.control_frame, text="Reset", command=self.reset_game, **control_style).pack(side=tk.LEFT, padx=10)
        tk.Button(self.control_frame, text="Exit", command=self.root.quit, **control_style).pack(side=tk.LEFT, padx=10)


    def draw_board(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                                    CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE)
            self.canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                                    CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE)

    def draw_piece(self, row, col, player):
        color = "black" if player == 1 else "white"
        x0 = col * CELL_SIZE + CELL_SIZE // 2 - 10
        y0 = row * CELL_SIZE + CELL_SIZE // 2 - 10
        x1 = col * CELL_SIZE + CELL_SIZE // 2 + 10
        y1 = row * CELL_SIZE + CELL_SIZE // 2 + 10
        self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def update_turn_label(self):
        if self.game_mode == 'ai_vs_ai':  
            if self.current_player == 1:
                self.turn_label.config(text="Black Turn")  
            else:
                self.turn_label.config(text="White Turn")  
        elif self.current_player == 1:
            self.turn_label.config(text="Black Turn")  
        else:
            self.turn_label.config(text="White Turn")  


    def start_ai_vs_ai(self):
        self.reset_board()
        self.game_mode = 'ai_vs_ai'
        self.root.after(100, self.ai_vs_ai_turn)

    def ai_vs_ai_turn(self):
        if self.check_game_end():
            return
        self.root.update()
        time.sleep(0.5)
        if self.current_player == 1:
            row, col = find_best_move_alphabeta(self.board, depth=2)
        else:
            row, col = find_best_move_minimax(self.board, depth=2)
        self.board[row][col] = self.current_player
        self.draw_piece(row, col, self.current_player)
        if not self.check_game_end():
            self.current_player = other_player(self.current_player)
            self.update_turn_label()
            self.root.after(100, self.ai_vs_ai_turn)

    def start_user_vs_ai(self):
        self.reset_board()
        self.game_mode = 'user_vs_ai'
        self.current_player = 1  # User "black" always starts

    def human_move(self, event):
        if self.game_mode != 'user_vs_ai' or self.current_player != 1:
            return

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if self.board[row][col] != 0:
            return

        self.board[row][col] = 1
        self.draw_piece(row, col, 1)

        if self.check_game_end():
            return

        self.current_player = 2
        self.update_turn_label()
        self.root.after(100, self.ai_move)

    def ai_move(self):
        if self.check_game_end():
            return
        row, col = find_best_move_minimax(self.board, depth=2)
        self.board[row][col] = 2
        self.draw_piece(row, col, 2)
        if not self.check_game_end():
            self.current_player = 1
            self.update_turn_label()

    def check_game_end(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] != 0:
                    if check_winner(self.board, i, j, self.board[i][j]):
                        winner = "Black" if self.board[i][j] == 1 else "White"
                        if self.game_mode == 'user_vs_ai':
                            winner = "You" if self.board[i][j] == 1 else "AI"
                        self.status_label.config(text=f"{winner} wins!")
                        return True

        if all(self.board[i][j] != 0 for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
            self.status_label.config(text="It's a draw!")
            return True

        return False

    def reset_board(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.canvas.delete("all")
        self.draw_board()
        self.current_player = 1

if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()


