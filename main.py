from hybrid_solver import parallel_hybrid_solver
from sudoku import SudokuBoard
import time
import multiprocessing
from genetic_algorithm import genetic_algorithm
from fuzzy_logic import fuzzy_logic_solver
from ant_colony import ant_colony_optimization
from backtracking_solver import solve_backtracking  # Import the backtracking solver

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

if __name__ == "__main__":
    # Define a Sudoku puzzle (0 represents empty cells)
    board = [
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 3],
        [0, 7, 4, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 0],
        [0, 0, 8, 0, 4, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 1, 9],
        [0, 0, 5, 0, 0, 0, 0, 0, 8]
    ]
    print("Initial Sudoku Board:")
    SudokuBoard("".join([str(x) for row in board for x in row])).print_board()
    print("-" * 25)
    print("generating please wait....")

    # First try backtracking
    board_copy = [row[:] for row in board]  # Deep copy
    start_time = time.time()
    if solve_backtracking(board_copy):
        SudokuBoard("".join([str(x) for row in board_copy for x in row])).print_board()
        print(f"Time taken: {time.time() - start_time:.4f} seconds")
    else:
        # If backtracking fails, fall back to hybrid solver
        print("Backtracking failed, trying hybrid solver...")
        solve_sudoku_hybrid(board)
