import random
from sudoku import SudokuBoard

def ant_colony_optimization(board_string, num_ants=10, num_iterations=100, alpha=1, beta=2, evaporation_rate=0.5):
    board = SudokuBoard(board_string)
    initial_board = board.get_board()
    pheromone = {}

   # Initialize pheromone levels
    for row in range(9):
        for col in range(9):
            if initial_board[row][col] == 0:
                for num in range(1, 10):
                    if board.is_valid(row, col, num):
                        pheromone[(row, col, num)] = 1

    def calculate_heuristic(row, col, num):
        # Heuristic: Number of empty cells that can be filled with 'num' in the same row, column, and box
        count = 1
        # Check row
        for j in range(9):
            if board.is_valid(row, j, num):
                count += 1
        # Check column
        for i in range(9):
            if board.is_valid(i, col, num):
                count += 1
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board.is_valid(start_row + i, start_col + j, num):
                    count += 1
        return count

    def ant_solution(board):
        new_board = [[initial_board[i][j] for j in range(9)] for i in range(9)]
        
        for row in range(9):
            for col in range(9):
                if new_board[row][col] == 0:
                    probabilities = {}
                    total_probability = 0
                    for num in range(1, 10):
                        if board.is_valid(row, col, num):
                            heuristic = calculate_heuristic(row, col, num)
                            probabilities[num] = (pheromone[(row, col, num)] ** alpha) * (heuristic ** beta)
                            total_probability += probabilities[num]

                    if total_probability == 0:
                        continue  # No valid moves, try next cell

                    # Choose a number based on probabilities
                    random_value = random.uniform(0, total_probability)
                    cumulative_probability = 0
                    for num, probability in probabilities.items():
                        cumulative_probability += probability
                        if random_value <= cumulative_probability:
                            new_board[row][col] = num
                            break
        return new_board

    # Main loop
    best_solution = None
    for iteration in range(num_iterations):
        solutions = []
        for _ in range(num_ants):
            new_board = ant_solution(board)
            if new_board:
                solutions.append(new_board)

        # Update pheromones
        for row in range(9):
            for col in range(9):
                if initial_board[row][col] == 0:
                    for num in range(1, 10):
                        if board.is_valid(row, col, num):
                            pheromone[(row, col, num)] *= (1 - evaporation_rate)  # Evaporation

        for solution in solutions:
            if solution:
                # Reward ants that found valid solutions
                reward = 1.0
                for row in range(9):
                    for col in range(9):
                        if initial_board[row][col] == 0:
                            num = solution[row][col]
                            if board.is_valid(row, col, num):
                                pheromone[(row, col, num)] += reward

                # Update best solution
                if best_solution is None:
                    best_solution = solution
                else:
                    # Check if the current solution is better than the best solution
                    is_better = True
                    for row in range(9):
                        for col in range(9):
                            if initial_board[row][col] == 0:
                                if solution[row][col] != best_solution[row][col]:
                                    is_better = False
                                    break
                        if not is_better:
                            break
                    if is_better:
                        best_solution = solution

    if best_solution:
        # Convert the solution to a SudokuBoard object
        solution_string = "".join([str(x) for row in best_solution for x in row])
        return SudokuBoard(solution_string)
    else:
        return None
