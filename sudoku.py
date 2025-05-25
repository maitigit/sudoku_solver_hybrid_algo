class SudokuBoard:
    def __init__(self, board_string):
        self.board = self.parse_board(board_string)

    def parse_board(self, board_string):
        board = []
        row = []
        for i, char in enumerate(board_string):
            if char == '0':
                row.append(0)
            else:
                row.append(int(char))
            if (i + 1) % 9 == 0:
                board.append(row)
                row = []
        return board

    def is_valid(self, row, col, num):
        # Check row
        for i in range(9):
            if self.board[row][i] == num:
                return False

        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def print_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - ")

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                print(self.board[i][j], end=" ")

            print()

    def is_solved(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
                if not self.is_valid(i, j, self.board[i][j]):
                    return False
        return True

    def get_board(self):
        return self.board
