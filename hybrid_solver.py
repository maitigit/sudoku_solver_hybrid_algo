import multiprocessing
from gpu_genetic_algorithm import parallel_genetic_algorithm
from fuzzy_logic import fuzzy_logic_solver
from ant_colony import ant_colony_optimization
from sudoku import SudokuBoard

def hybrid_solver(board_string, num_processes=4):
    # 1. Genetic Algorithm (Parallel)
    ga_result = parallel_genetic_algorithm(board_string, population_size=500, num_generations=2000, mutation_rate=0.3)
    if ga_result is not None and ga_result.is_solved():
        return ga_result
    elif ga_result is not None and len(ga_result.get_board()) > 0:
        board = ga_result
    else:
        board = SudokuBoard(board_string)

    if board is not None:
        # 2. Fuzzy Logic (Refinement)
        fl_result = fuzzy_logic_solver("".join([str(x) for row in board.get_board() for x in row]))
        if fl_result is not None and fl_result.is_solved():
             return fl_result
        elif fl_result is not None:
            board = fl_result

        # 3. Ant Colony Optimization (Optimization)
        aco_result = ant_colony_optimization("".join([str(x) for row in board.get_board() for x in row]))
        if aco_result and aco_result.is_solved():
            return aco_result
        elif aco_result:
             board = aco_result

    if board is not None and board.is_solved():
        return board
    else:
        return board  # Return the best board found so far, even if not solved

def parallel_hybrid_solver(board_string, num_processes=4):
    board_strings = [board_string] * num_processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(hybrid_solver, board_strings)
    best_solution = None
    for result in results:
        if result and result.is_solved():
            return result
        elif result:
            if best_solution is None:
                best_solution = result
            elif calculate_fitness(result) > calculate_fitness(best_solution):
                best_solution = result
    if best_solution and best_solution.is_solved():
        return best_solution
    elif best_solution:
        return best_solution
    else:
        return None

def calculate_fitness(board):
    violations = 0
    for i in range(9):
        row_values = []
        col_values = []
        for j in range(9):
            if board.get_board()[i][j] != 0:
                if board.get_board()[i][j] in row_values:
                    violations += 1
                else:
                    row_values.append(board.get_board()[i][j])
            if board.get_board()[j][i] != 0:
                if board.get_board()[j][i] in col_values:
                    violations += 1
                else:
                    col_values.append(board.get_board()[j][i])
    for box_row in range(3):
        for box_col in range(3):
            box_values = []
            for i in range(3):
                for j in range(3):
                    row = box_row * 3 + i
                    col = box_col * 3 + j
                    if board.get_board()[row][col] != 0:
                        if board.get_board()[row][col] in box_values:
                            violations += 1
                        else:
                            box_values.append(board.get_board()[row][col])
    return -violations  # Higher fitness is better
