import tkinter as tk
import math

HUMAN = 'X'
AI = 'O'
EMPTY = ' '

def create_board():
    return [EMPTY] * 9

def get_winner(board):
    win_positions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]
    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    return None

def is_full(board):
    return all(cell != EMPTY for cell in board)

def evaluate(board):
    winner = get_winner(board)
    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    return 0

def minimax(board, depth, alpha, beta, is_maximizing):
    score = evaluate(board)
    if score == 1 or score == -1 or is_full(board):
        return score

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                eval_value = minimax(board, depth + 1, alpha, beta, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                eval_value = minimax(board, depth + 1, alpha, beta, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            move_val = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = EMPTY
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Minimax)")
        self.root.configure(bg="#041a2c")
        self.root.resizable(False, False)

        self.board = create_board()
        self.buttons = []

        main_frame = tk.Frame(root, bg="#d5e3f0", padx=15, pady=15, bd=2, relief="ridge")
        main_frame.grid(row=0, column=0)

        self.status_label = tk.Label(
            main_frame,
            text="You are X. Your turn!",
            font=("Segoe UI", 13, "bold"),
            bg="#b6cbe3",
            fg="#2c3e50",
            pady=8,
            padx=10,
            width=25
        )
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        for i in range(9):
            btn = tk.Button(
                main_frame,
                text="",
                font=("Segoe UI", 22, "bold"),
                width=4,
                height=2,
                bg="#f4f9ff",
                activebackground="#cfe0f5",
                relief="groove",
                bd=3,
                command=lambda idx=i: self.on_button_click(idx)
            )
            btn.grid(row=1 + (i // 3), column=i % 3, padx=7, pady=7)
            self.buttons.append(btn)

        self.restart_button = tk.Button(
            main_frame,
            text="⟳ Restart Game",
            font=("Segoe UI", 11, "bold"),
            bg="#aac6df",
            fg="#1b2a41",
            activebackground="#8fb7d5",
            width=20,
            pady=5,
            command=self.restart_game
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=(12, 0))

        self.game_over = False

    def on_button_click(self, index):
        if self.game_over:
            return

        if self.board[index] == EMPTY:
            self.board[index] = HUMAN
            self.update_buttons()

            if self.check_game_state():
                return

            self.status_label.config(text="AI is thinking...")
            self.root.update_idletasks()

            ai_index = best_move(self.board)
            if ai_index is not None:
                self.board[ai_index] = AI
                self.update_buttons()
                self.check_game_state()

    def update_buttons(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])
            if self.board[i] == HUMAN:
                self.buttons[i].config(fg="#1565c0")
            elif self.board[i] == AI:
                self.buttons[i].config(fg="#c62828")

    def check_game_state(self):
        winner = get_winner(self.board)

        if winner:
            if winner == HUMAN:
                self.status_label.config(text="🎉 You Win!")
            elif winner == AI:
                self.status_label.config(text="🤖 AI Wins!")

            self.highlight_winner()
            self.game_over = True
            self.disable_all_buttons()
            return True

        elif is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!")
            self.game_over = True
            self.disable_all_buttons()
            return True

        self.status_label.config(text="Your turn (X).")
        return False

    def highlight_winner(self):
        win_positions = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]

        for a,b,c in win_positions:
            if self.board[a] == self.board[b] == self.board[c] != EMPTY:
                for idx in (a, b, c):
                    self.buttons[idx].config(bg="#ffeb99")

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)

    def restart_game(self):
        self.board = create_board()
        self.game_over = False

        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, bg="#f4f9ff")

        self.status_label.config(text="New Game! You are X. Your turn!")

    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Minimax)")
        self.root.resizable(False, False)

        self.board = create_board()
        self.buttons = []

        self.status_label = tk.Label(
            root,
            text="You are X. Your turn!",
            font=("Segoe UI", 12, "bold"),
            pady=10
        )
        self.status_label.grid(row=0, column=0, columnspan=3)

        for i in range(9):
            btn = tk.Button(
                root,
                text="",
                font=("Segoe UI", 20, "bold"),
                width=4,
                height=2,
                command=lambda idx=i: self.on_button_click(idx)
            )
            btn.grid(row=1 + (i // 3), column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.restart_button = tk.Button(
            root,
            text="Restart",
            font=("Segoe UI", 10, "bold"),
            command=self.restart_game
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=(5, 10))

        self.game_over = False

    def on_button_click(self, index):
        if self.game_over:
            return

        if self.board[index] == EMPTY:
            self.board[index] = HUMAN
            self.update_buttons()

            if self.check_game_state():
                return

            self.status_label.config(text="AI is thinking...")
            self.root.update_idletasks()

            ai_index = best_move(self.board)
            if ai_index is not None and self.board[ai_index] == EMPTY:
                self.board[ai_index] = AI
                self.update_buttons()
                self.check_game_state()

    def update_buttons(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])
            if self.board[i] == HUMAN:
                self.buttons[i].config(fg="#1e90ff")
            elif self.board[i] == AI:
                self.buttons[i].config(fg="#e74c3c")

    def check_game_state(self):
        winner = get_winner(self.board)
        if winner == HUMAN:
            self.status_label.config(text="You win! 🎉 (Rare!)")
            self.game_over = True
            self.disable_all_buttons()
            return True
        elif winner == AI:
            self.status_label.config(text="AI wins! 🤖 Unbeatable!")
            self.game_over = True
            self.disable_all_buttons()
            return True
        elif is_full(self.board):
            self.status_label.config(text="It's a draw! 🤝")
            self.game_over = True
            self.disable_all_buttons()
            return True
        else:
            self.status_label.config(text="Your turn (X).")
            return False

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)

    def restart_game(self):
        self.board = create_board()
        self.game_over = False
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL)
        self.status_label.config(text="New game! You are X. Your turn!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
