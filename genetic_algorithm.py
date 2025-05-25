import random
from sudoku import SudokuBoard

def generate_population(population_size, board_string):
    initial_board = SudokuBoard(board_string)
    initial_values = initial_board.get_board()
    population = []
    for _ in range(population_size):
        board = [[initial_values[i][j] for j in range(9)] for i in range(9)]
        # Fill empty cells with random numbers (1-9)
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    board[i][j] = random.randint(1, 9)
                    
        population.append(SudokuBoard("".join([str(x) for row in board for x in row])))

    return population

def calculate_fitness(board):
    # Calculate the number of constraint violations and penalize empty cells
    violations = 0
    empty_cells = 0

    # Check row and column constraints
    for i in range(9):
        row_values = set()
        col_values = set()
        for j in range(9):
            val_row = board.get_board()[i][j]
            val_col = board.get_board()[j][i]
            if val_row == 0:
                empty_cells += 1
            else:
                if val_row in row_values:
                    violations += 1
                row_values.add(val_row)
            if val_col != 0:
                if val_col in col_values:
                    violations += 1
                col_values.add(val_col)

    # Check 3x3 box constraints
    for box_row in range(3):
        for box_col in range(3):
            box_values = set()
            for i in range(3):
                for j in range(3):
                    row = box_row * 3 + i
                    col = box_col * 3 + j
                    val = board.get_board()[row][col]
                    if val == 0:
                        continue
                    if val in box_values:
                        violations += 1
                    box_values.add(val)

    # Penalize empty cells heavily
    return -(violations + 10 * empty_cells)

def selection(population, fitnesses, num_parents):
    # Select the best individuals for reproduction
    parents = []
    for _ in range(num_parents):
        max_fitness_idx = fitnesses.index(max(fitnesses))
        parents.append(population[max_fitness_idx])
        fitnesses[max_fitness_idx] = float('-inf')  # Ensure the same parent is not selected again
    return parents

def crossover(parent1, parent2):
    # Create offspring by combining the genetic material of two parents
    offspring_board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if random.random() < 0.5:
                offspring_board[i][j] = parent1.get_board()[i][j]
            else:
                offspring_board[i][j] = parent2.get_board()[i][j]
    return SudokuBoard("".join([str(x) for row in offspring_board for x in row]))

def mutate(board, mutation_rate, initial_board):
    # Introduce random changes into the offspring
    new_board = board.get_board()
    initial_vals = initial_board.get_board()
    for i in range(9):
        for j in range(9):
            if initial_vals[i][j] == 0 and random.random() < mutation_rate:
                valid_numbers = [n for n in range(1, 10) if board.is_valid(i, j, n)]
                if valid_numbers:
                    new_board[i][j] = random.choice(valid_numbers)
    board = SudokuBoard("".join([str(x) for row in new_board for x in row]))
    return board

def genetic_algorithm(board_string, population_size=100, num_generations=100, mutation_rate=0.1):
    initial_board = SudokuBoard(board_string)
    population = generate_population(population_size, board_string)
    if population is None:
        return None

    for generation in range(num_generations):
        fitnesses = [calculate_fitness(board) for board in population]
        if max(fitnesses) == 0:
            #   print("Solution found")
            return population[fitnesses.index(max(fitnesses))]

        parents = selection(population, fitnesses.copy(), population_size // 2)

        offspring = []
        while len(offspring) < population_size - len(parents):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, initial_board)
            offspring.append(child)

        population = parents + offspring

    
    return None
