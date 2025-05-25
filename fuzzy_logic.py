import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from sudoku import SudokuBoard

def fuzzy_logic_solver(board_string):
    board = SudokuBoard(board_string)
    initial_board = [row[:] for row in board.get_board()]

    # Define fuzzy variables
    row_validity = ctrl.Antecedent(np.arange(0, 10, 1), 'row_validity')
    col_validity = ctrl.Antecedent(np.arange(0, 10, 1), 'col_validity')
    box_validity = ctrl.Antecedent(np.arange(0, 10, 1), 'box_validity')
    cell_value = ctrl.Consequent(np.arange(1, 10, 1), 'cell_value')

    # Define membership functions
    row_validity['low'] = fuzz.trimf(row_validity.universe, [0, 0, 5])
    row_validity['medium'] = fuzz.trimf(row_validity.universe, [0, 5, 10])
    row_validity['high'] = fuzz.trimf(row_validity.universe, [5, 10, 10])

    col_validity['low'] = fuzz.trimf(col_validity.universe, [0, 0, 5])
    col_validity['medium'] = fuzz.trimf(col_validity.universe, [0, 5, 10])
    col_validity['high'] = fuzz.trimf(col_validity.universe, [5, 10, 10])

    box_validity['low'] = fuzz.trimf(box_validity.universe, [0, 0, 5])
    box_validity['medium'] = fuzz.trimf(box_validity.universe, [0, 5, 10])
    box_validity['high'] = fuzz.trimf(box_validity.universe, [5, 10, 10])

    cell_value['1'] = fuzz.trimf(cell_value.universe, [1, 1, 1])
    cell_value['2'] = fuzz.trimf(cell_value.universe, [2, 2, 2])
    cell_value['3'] = fuzz.trimf(cell_value.universe, [3, 3, 3])
    cell_value['4'] = fuzz.trimf(cell_value.universe, [4, 4, 4])
    cell_value['5'] = fuzz.trimf(cell_value.universe, [5, 5, 5])
    cell_value['6'] = fuzz.trimf(cell_value.universe, [6, 6, 6])
    cell_value['7'] = fuzz.trimf(cell_value.universe, [7, 7, 7])
    cell_value['8'] = fuzz.trimf(cell_value.universe, [8, 8, 8])
    cell_value['9'] = fuzz.trimf(cell_value.universe, [9, 9, 9])

    # Define rules
    rule1 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['1'])
    rule2 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['2'])
    rule3 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['3'])
    rule4 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['4'])
    rule5 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['5'])
    rule6 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['6'])
    rule7 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['7'])
    rule8 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['8'])
    rule9 = ctrl.Rule(row_validity['high'] & col_validity['high'] & box_validity['high'], cell_value['9'])
    
    rule10 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['1'])
    rule11 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['2'])
    rule12 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['3'])
    rule13 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['4'])
    rule14 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['5'])
    rule15 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['6'])
    rule16 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['7'])
    rule17 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['8'])
    rule18 = ctrl.Rule(row_validity['medium'] & col_validity['medium'] & box_validity['medium'], cell_value['9'])

    # Control system
    cell_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18])
    cell_sim = ctrl.ControlSystemSimulation(cell_ctrl)

    # Solve the Sudoku using fuzzy logic
    for row in range(9):
        for col in range(9):
            if initial_board[row][col] == 0:
                possible_values = []
                for num in range(1, 10):
                    if board.is_valid(row, col, num):
                        possible_values.append(num)

                if possible_values:
                    # Evaluate fuzzy rules for each possible value
                    value_scores = {}
                    for num in possible_values:
                        # Calculate row, column, and box validity
                        row_violations = 0
                        for i in range(9):
                            if initial_board[row][i] == num:
                                row_violations += 1
                        row_validity_score = 10 - row_violations

                        col_violations = 0
                        for i in range(9):
                            if initial_board[i][col] == num:
                                col_violations += 1
                        col_validity_score = 10 - col_violations

                        box_violations = 0
                        start_row = row - row % 3
                        start_col = col - col % 3
                        for i in range(3):
                            for j in range(3):
                                if initial_board[start_row + i][start_col + j] == num:
                                    box_violations += 1
                        box_validity_score = 10 - box_violations

                        # Pass inputs to the control system
                        cell_sim.input['row_validity'] = row_validity_score
                        cell_sim.input['col_validity'] = col_validity_score
                        cell_sim.input['box_validity'] = box_validity_score

                        # Compute
                        cell_sim.compute()

                        # Get the fuzzy output
                        value_scores[num] = cell_sim.output['cell_value']

                    # Choose the value with the highest score
                    best_value = max(value_scores, key=value_scores.get)
                    board.get_board()[row][col] = best_value

    return board
