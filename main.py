from hybrid_solver import parallel_hybrid_solver
from sudoku import SudokuBoard
import time
import multiprocessing
from genetic_algorithm import genetic_algorithm
from fuzzy_logic import fuzzy_logic_solver
from ant_colony import ant_colony_optimization
from backtracking_solver import solve_backtracking  # Import the backtracking solver
import json
import sys
import sqlite3

def solve_sudoku_hybrid(board):
    # Solve the Sudoku puzzle using the parallel hybrid solver
    start_time = time.time()
    board_string = "".join([str(x) for row in board for x in row])
    solved_board = parallel_hybrid_solver(board_string)
    end_time = time.time()
    if solved_board:
        solved_board.print_board()
        print(f"Time taken: {end_time - start_time:.4f} seconds")
    return solved_board

def load_board_from_json(file_path, board_index=0):
    
    try:
        with open(file_path, 'r') as f:
            boards = json.load(f)
            if not boards:
                print(f"Error: No boards found in {file_path}")
                return None
            if 0 <= board_index < len(boards):
                puzzle_obj = boards[board_index]
                return puzzle_obj['id'], puzzle_obj['board']
            else:
                print(f"Error: Invalid board index {board_index}. Available boards: 0 to {len(boards) - 1}.")
                return None
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def initialize_database(db_path="sudoku_results.db"):
    """Initializes the SQLite database and creates the results table if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solve_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                puzzle_id INTEGER,
                puzzle_string TEXT NOT NULL,
                time_taken REAL NOT NULL
            );
        """)
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    json_file_path = "sudoku_boards.json"
    selected_board_index = 0 # Default to the first board
    if len(sys.argv) > 1:
        try:
            selected_board_index = int(sys.argv[1])
        except ValueError:
            print("Error: Invalid board index provided. Using the first board (index 0).")
            selected_board_index = 0

    result = load_board_from_json(json_file_path, selected_board_index)
    if result is None:
        exit() # Exit if board loading failed
    puzzle_id, board = result

    print(f"Initial Sudoku Board (ID: {puzzle_id}):")
    SudokuBoard("".join([str(x) for row in board for x in row])).print_board()
    print("-" * 25)
    print("generating please wait....")

    # BT
    board_copy = [row[:] for row in board]  
    start_time = time.time()
    
    solved_board_data = None
    time_elapsed = 0

    if solve_backtracking(board_copy):
        solved_board_data = board_copy
        time_elapsed = time.time() - start_time
        SudokuBoard("".join([str(x) for row in solved_board_data for x in row])).print_board()
        print(f"Time taken : {time_elapsed:.4f} seconds")
    else:
       #
        print("Backtracking failed, trying hybrid solver...")
        start_time_hybrid = time.time()
        solved_board_data_hybrid = solve_sudoku_hybrid(board)
        time_elapsed_hybrid = time.time() - start_time_hybrid
        if solved_board_data_hybrid:
             solved_board_data = [list(map(int,list(solved_board_data_hybrid.board_string[i:i+9]))) for i in range(0,81,9)]
             time_elapsed = time_elapsed_hybrid

    # Save results to database if a board was solved
    if solved_board_data:
        db_path = "sudoku_results.db"
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            puzzle_string = "".join([str(x) for row in board for x in row])
            time_elapsed_str = "{:.3f}".format(time_elapsed)
            cursor.execute("INSERT INTO solve_results (puzzle_id, puzzle_string, time_taken) VALUES (?, ?, ?)",
                           (puzzle_id, puzzle_string, time_elapsed_str))
            conn.commit()
            print("Results saved to database.")
        except sqlite3.Error as e:
            print(f"Database error while saving results: {e}")
        finally:
            if conn:
                conn.close()
