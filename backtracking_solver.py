from sudoku import SudokuBoard

def find_empty(board):
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_backtracking(board):
    
    empty = find_empty(board)
    if not empty:
        # No empty cell left, puzzle solved
        return True
    row, col = empty
    for num in range(1, 10):
        # Check if num is valid in this position
        if SudokuBoard("".join([str(x) for row in board for x in row])).is_valid(row, col, num):
            board[row][col] = num
            if solve_backtracking(board):
                return True
            # Undo assignment (backtrack)
            board[row][col] = 0
    # No valid number found, trigger backtracking
    return False 