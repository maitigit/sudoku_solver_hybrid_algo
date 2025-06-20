import numpy as np
from sudoku import SudokuBoard
import random
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def calculate_fitness_parallel(board_data):
    board, idx = board_data
    violations = 0
    empty_cells = 0
    
    # Check rows and columns
    for i in range(9):
        row_values = [0] * 10  # 0-9
        col_values = [0] * 10
        for j in range(9):
            val_row = board[i * 9 + j]
            val_col = board[j * 9 + i]
            
            if val_row == 0:
                empty_cells += 1
            else:
                if row_values[val_row] > 0:
                    violations += 1
                row_values[val_row] += 1
                
            if val_col != 0:
                if col_values[val_col] > 0:
                    violations += 1
                col_values[val_col] += 1
    
    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            box_values = [0] * 10
            for i in range(3):
                for j in range(3):
                    row = box_row * 3 + i
                    col = box_col * 3 + j
                    val = board[row * 9 + col]
                    if val != 0:
                        if box_values[val] > 0:
                            violations += 1
                        box_values[val] += 1
    
    return idx, -(violations + 10 * empty_cells)

def parallel_genetic_algorithm(board_string, population_size=500, num_generations=2000, mutation_rate=0.3):
    # Convert initial board to numpy array
    initial_board = SudokuBoard(board_string)
    initial_values = np.array([int(x) for x in board_string], dtype=np.int32)
    
    # Generate initial population
    population = np.zeros((population_size, 81), dtype=np.int32)
    for i in range(population_size):
        board = initial_values.copy()
        empty_cells = np.where(board == 0)[0]
        board[empty_cells] = np.random.randint(1, 10, size=len(empty_cells))
        population[i] = board
    
    # Get number of CPU cores
    num_cores = multiprocessing.cpu_count()
    
    for generation in range(num_generations):
        # Calculate fitness in parallel
        with ThreadPoolExecutor(max_workers=num_cores) as executor:
            fitness_results = list(executor.map(calculate_fitness_parallel, 
                                             [(population[i], i) for i in range(population_size)]))
        
        # Sort results by index and extract fitness scores
        fitness_results.sort(key=lambda x: x[0])
        fitness_scores = np.array([score for _, score in fitness_results])
        
        # Check if solution found
        max_fitness = np.max(fitness_scores)
        if max_fitness == 0:
            best_idx = np.argmax(fitness_scores)
            solution = population[best_idx]
            return SudokuBoard("".join(map(str, solution)))
        
        # Selection
        sorted_indices = np.argsort(fitness_scores)[::-1]
        parents = population[sorted_indices[:population_size//2]]
        
        # Crossover
        offspring = np.zeros_like(population)
        for i in range(0, population_size//2, 2):
            if i + 1 < len(parents):
                crossover_point = np.random.randint(0, 81)
                offspring[i] = np.concatenate([parents[i][:crossover_point], 
                                            parents[i+1][crossover_point:]])
                offspring[i+1] = np.concatenate([parents[i+1][:crossover_point], 
                                              parents[i][crossover_point:]])
        
        # Mutation
        for i in range(population_size//2):
            for j in range(81):
                if initial_values[j] == 0 and np.random.random() < mutation_rate:
                    offspring[i, j] = np.random.randint(1, 10)
        
        # Update population
        population = np.concatenate([parents, offspring])
    
    # Return best solution found
    with ThreadPoolExecutor(max_workers=num_cores) as executor:
        fitness_results = list(executor.map(calculate_fitness_parallel, 
                                         [(population[i], i) for i in range(population_size)]))
    fitness_results.sort(key=lambda x: x[0])
    fitness_scores = np.array([score for _, score in fitness_results])
    best_idx = np.argmax(fitness_scores)
    solution = population[best_idx]
    return SudokuBoard("".join(map(str, solution))) 