import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import sqlite3
from sudoku import SudokuBoard
from backtracking_solver import solve_backtracking
from hybrid_solver import parallel_hybrid_solver

JSON_PATH = "sudoku_boards.json"

# Load all puzzles from JSON
with open(JSON_PATH, 'r') as f:
    PUZZLES = json.load(f)

def save_result_to_db(puzzle_id, puzzle_string, time_taken):
    conn = sqlite3.connect("sudoku_results.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solve_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puzzle_id INTEGER,
            puzzle_string TEXT NOT NULL,
            time_taken REAL NOT NULL
        );
    """)
    cursor.execute(
        "INSERT INTO solve_results (puzzle_id, puzzle_string, time_taken) VALUES (?, ?, ?)",
        (puzzle_id, puzzle_string, "{:.3f}".format(time_taken))
    )
    conn.commit()
    conn.close()

class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Visual Solver")
        self.geometry("700x600")
        self.configure(bg="#f4f4f4")
        self.selected_index = tk.StringVar(value="ID 0")
        self.solved_board = None
        self.time_taken = None
        self.create_widgets()
        self.display_board(PUZZLES[0]['board'])

    def create_widgets(self):
        # Title
        tk.Label(self, text="Sudoku Visual Solver", font=("Helvetica", 22, "bold"), bg="#f4f4f4", fg="#333").pack(pady=10)
        # Puzzle selector
        selector_frame = tk.Frame(self, bg="#f4f4f4")
        selector_frame.pack(pady=5)
        tk.Label(selector_frame, text="Select Test Case:", font=("Helvetica", 12), bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
        self.puzzle_menu = ttk.Combobox(selector_frame, state="readonly", width=10,
            values=[f"ID {p['id']}" for p in PUZZLES],
            textvariable=self.selected_index)
        self.puzzle_menu.current(0)
        self.puzzle_menu.pack(side=tk.LEFT, padx=5)
        self.puzzle_menu.bind("<<ComboboxSelected>>", self.on_select)
        # Solve button
        self.solve_btn = ttk.Button(selector_frame, text="Solve", command=self.solve)
        self.solve_btn.pack(side=tk.LEFT, padx=10)
        # Time label
        self.time_label = tk.Label(selector_frame, text="", font=("Helvetica", 12), bg="#f4f4f4", fg="#2a4d69")
        self.time_label.pack(side=tk.LEFT, padx=10)
        # Board frame
        self.board_frame = tk.Frame(self, bg="#f4f4f4")
        self.board_frame.pack(pady=20)
        # Status
        self.status_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#f4f4f4", fg="#c0392b")
        self.status_label.pack(pady=5)

    def display_board(self, board, solved=False):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                cell_bg = "#eaf6ff" if (r//3+c//3)%2==0 else "#f9f9f9"
                fg = "#333" if val != 0 else "#bbb"
                font = ("Consolas", 16)
                padx = 2
                pady = 2
                if c in [3, 6]:
                    padx = (10, 2)  # extra space before col 3 and 6
                if r in [3, 6]:
                    pady = (10, 2)  # extra space before row 3 and 6
                cell = tk.Label(self.board_frame, text=str(val) if val != 0 else '', width=3, height=2, font=font, bg=cell_bg, fg=fg, relief="ridge", borderwidth=2)
                cell.grid(row=r, column=c, padx=padx, pady=pady)

    def on_select(self, event=None):
        idx = self.puzzle_menu.current()
        self.solved_board = None
        self.time_label.config(text="")
        self.status_label.config(text="")
        self.display_board(PUZZLES[idx]['board'])

    def solve(self):
        idx = self.puzzle_menu.current()
        board = [row[:] for row in PUZZLES[idx]['board']]
        self.status_label.config(text="Solving...")
        self.update()
        start = time.time()
        solved = False
        if solve_backtracking(board):
            solved = True
        else:
            # Try hybrid
            result = parallel_hybrid_solver("".join([str(x) for row in PUZZLES[idx]['board'] for x in row]))
            if result:
                board = [list(map(int, list(result.board_string[i:i+9]))) for i in range(0,81,9)]
                solved = True
        elapsed = time.time() - start
        if solved:
            self.solved_board = board
            self.display_board(board, solved=True)
            self.time_label.config(text=f"Solved in {elapsed:.3f} s")
            self.status_label.config(text="Solved!")
            # Save to database
            puzzle_id = PUZZLES[idx]['id']
            puzzle_string = "".join([str(x) for row in PUZZLES[idx]['board'] for x in row])
            save_result_to_db(puzzle_id, puzzle_string, elapsed)
        else:
            self.status_label.config(text="No solution found.")
            self.time_label.config(text="")

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop() 