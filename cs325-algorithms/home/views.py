from django.shortcuts import render
from django.http import HttpResponse
import random
# from struct import sudoku

def home(request):
    return render(request, 'home/home.html')

def puzzle(request):
    return render(request, 'home/puzzle.html')

def puzzle_solved(request):
    return render(request, 'home/puzzle_solved.html')

def check(request):
    # get Sudoku 3x3 squares and check them
    squares = get_squares(request.GET)
    squares_test = verify(squares)
    # get Sudoku 1x9 rows and check them
    rows = get_rows(request.GET)
    rows_test = verify(rows)
    # get Sudoku 9x1 columns and check them
    cols = get_cols(request.GET)
    cols_test = verify(cols)
    # determine whether all tests passed
    print(squares_test)
    print(cols_test)
    print(rows_test)
    valid_puzzle = squares_test and rows_test and cols_test
    # prepare context to pass to template
    context = {}
    if valid_puzzle:
        context["valid"] = True
        context["note"] = "Great Job! That puzzle was valid!"
    else:
        context["valid"] = False
        context["note"] = "Whoops, that puzzle was not valid!"
    return render(request, 'home/check.html', context)

class SudokuBoard:
    """
    represents a 9x9 sudoku board
    generating algorithm: https://stackoverflow.com/questions/6924216/how-to-generate-sudoku-boards-with-unique-solutions#:~:text=Start%20with%20an%20empty%20board,at%20least%20one%20valid%20solution.
    """
    def __init__(self, n):
        self.n = n
        self.rows = [SudokuRow(n)] * (n**2)
        self.cols = [SudokuCol(n)] * (n**2)
        self.squares = [SudokuSquare(n)] * (n**2)
        self.count = n**4
        self.solved = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 1, 5, 6, 4, 8, 9, 7],
            [5, 6, 4, 8, 9, 7, 2, 3, 1],
            [8, 9, 7, 2, 3, 1, 5, 6, 4],
            [3, 1, 2, 6, 4, 5, 9, 7, 8],
            [6, 4, 5, 9, 7, 8, 3, 1, 2],
            [9, 7, 8, 3, 1, 2, 6, 4, 5]
        ]
        # shuffle starting board to generate random valid board
        self.shuffle_vals()
        self.shuffle_rows()
        self.shuffle_columns()
        self.shuffle_row_blocks()
        self.shuffle_column_blocks()
        self.grid = self.solved

    def build_starting_grid(self):
        # use set to keep track of removed cells
        visited = set()


    def shuffle_column_blocks(self):
        # seed the random number generator
        random.seed
        for j in range(self.n):
            adj = random.randint(0, self.n - 1)
            for i in range(self.n):
                self.swap_columns(j * self.n + i, adj * self.n + i)

    def shuffle_row_blocks(self):
        # seed the random number generator
        random.seed
        for i in range(self.n):
            adj = random.randint(0, self.n - 1)
            for j in range(self.n):
                self.swap_rows(i * self.n + j, adj * self.n + j)

    def shuffle_columns(self):
        # seed the random number generator
        random.seed
        for j in range(self.n**2):
            adj = random.randint(0, self.n - 1)
            new = (j // 3 * 3) + adj
            self.swap_columns(j, new)

    def shuffle_rows(self):
        # seed the random number generator
        random.seed
        for i in range(self.n**2):
            adj = random.randint(0, self.n - 1)
            new = (i // 3 * 3) + adj
            self.swap_rows(i, new)

    def swap_columns(self, c1, c2):
        for i in range(self.n**2):
            self.solved[i][c1], self.solved[i][c2] = self.solved[i][c2], self.solved[i][c1]

    def swap_rows(self, r1, r2):
        self.solved[r1], self.solved[r2] = self.solved[r2], self.solved[r1]

    def shuffle_vals(self):
        # seed the random number generator
        random.seed
        for i in range(1, 10):
            rep = random.randint(1, 9)
            for r in range(len(self.solved)):
                for c in range(len(self.solved[0])):
                    if self.solved[r][c] == rep:
                        self.solved[r][c] = i
                    elif self.solved[r][c] == i:
                        self.solved[r][c] = rep

    def gen_solved_board(self):
        """
        DESCRIPTION:    builds a random fully populated (solved) sudoku board
                        via guess and check

        INPUT:          NA

        RETURN:         NA, populates object's properties/fields
        """
        # seed the random number generator
        random.seed
        # continue randomly placing values until board is fully populated
        row = col = val = None
        while self.count < self.n**4:
            # get a random value, row, and column to place
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            val = random.randint(1, 9)
            # print('row: ', row)
            # print('col: ', col)
            # print('val: ', val)
            # calculate square index
            sq = (row // 3) * 3 + (col // 3)
            # print('sq: ', sq)
            # handle case of valid placement
            if self.placement_is_valid(row, col, sq, val):
                self.place_val(row, col, sq, val)
                self.board[row][col] = val
                self.count += 1


    def place_val(self, row, col, sq, val):
        """
        DESCRIPTION:    

        INPUT:          

        RETURN:         
        """
        # place vals in groups
        for group in [self.rows[row], self.cols[col], self.squares[sq]]:
            group.place_val(val)

    def placement_is_valid(self, row, col, sq, val):
        """
        DESCRIPTION:    

        INPUT:          

        RETURN:         
        """
        # determine if val is already placed for any grouping
        groups = [self.rows[row], self.cols[col], self.squares[sq]]
        for group in groups:
            if group.val_is_placed(val):
                return False
        # all groupings valid, indicate to calling function
        return True
        


class SudokuGroup:
    """
    represents a grouping of cells on a sudoku board
    """
    def __init__(self, n):
        self.n = n
        self.values = set()
        self.complete = False

    def place_val(self, val):
        """
        DESCRIPTION:    adds a number to the grouping's values property

        INPUT:          val (int): value being added to the group

        RETURN:         boolean indication of successful add
        """
        # handle case of value already added
        if val in self.values:
            return False
        # handle case of eligible value
        self.values.add(val)
        # update complete property, if applicable
        if len(self.values) == self.n**2:
            self.complete = True
        return True

    def val_is_placed(self, val):
        """
        DESCRIPTION:    

        INPUT:          

        RETURN:         
        """
        return val in self.values

class SudokuRow(SudokuGroup):
    """
    represents a row on a n x n sudoku board
    """
    

class SudokuCol(SudokuGroup):
    """
    represents a column on a n x n sudoku board
    """
    

class SudokuSquare(SudokuGroup):
    """
    represents a square on a n x n sudoku board
    """
    


def puzz(request):
    """
    DESCRIPTION:    builds valid starting sudoku puzzle 2D array

    INPUT:          request: GET request for /puzzle

    RETURN:         Sudoku column and row values
    """
    # build array skeleton
    res = [[None] * 9 for _ in range(9)]


def get_rows(query_dict: {}) -> []:
    """
    DESCRIPTION:    parses request parameters and returns
                    sudoku rows to user / calling function.
    INPUT:          query string dictionary
    RETURN:         Sudoku row values
    """
    matrix = []
    # loop through rows
    for i in range(1, 10, 1):
        temp_arr = []
        # loop through columns
        for j in range(1, 10, 1):
            # build string key using indices
            key = str(i) + str(j)
            temp_arr.append(query_dict[key])
        # make shallow copy of list to add to matrix
        copy = temp_arr.copy()
        matrix.append(copy)
    # return list of row values to calling function/user
    return matrix

def get_squares(query_dict: {}) -> []:
    """
    DESCRIPTION:    parses request parameters and returns
                    sudoku squares to user / calling function.
    INPUT:          query string dictionary
    RETURN:         Sudoku square values
    """
    matrix = []
    # set row iterator for 3-element chunks
    x = 0
    while x < 7:
        # set column iterator for 3-element chunks
        y = 0
        while y < 7:
            temp_arr = []
            # loop through three rows
            for i in range(x + 1, x + 4, 1):
                # loop through three columns
                for j in range(y + 1, y + 4, 1):
                    # build string key using indices
                    key = str(i) + str(j)
                    temp_arr.append(query_dict[key])
            # make shallow copy of list to add to matrix
            copy = temp_arr.copy()
            matrix.append(copy)
            # iterate 3 columns over
            y += 3
        # iterate 3 rows over
        x += 3
    # return list of row values to calling function/user
    return matrix


def get_cols(query_dict: {}) -> []:
    """
    DESCRIPTION:    parses request parameters and returns
                    sudoku columns to user / calling function.
    INPUT:          query string dictionary
    RETURN:         Sudoku column values
    """
    matrix = []
    # loop through rows
    for i in range(1, 10, 1):
        temp_arr = []
        # loop through columns
        for j in range(1, 10, 1):
            # build string key using indices
            key = str(j) + str(i)
            temp_arr.append(query_dict[key])
        # make shallow copy of list to add to matrix
        copy = temp_arr.copy()
        matrix.append(copy)
    # return list of row values to calling function/user
    return matrix

def verify(matrix: []) -> bool:
    """
    DESCRIPTION:    verifies that each list in the matrix
                    contains the numbers 1-9 exactly once
    INPUT:          matrix of column, row, or square values
                    in a Sudoku puzzle
    RETURN:         boolean indication of whether each list
                    passes Sudoku criteria
    """
    # loop through each list in the matrix
    for row in matrix:
        dict = {'1': None, '2': None, '3': None,
                '4': None, '5': None, '6': None,
                '7': None, '8': None, '9': None}
        # loop through each element in row
        for elt in row:
            # handle case where value is out of range
            if elt == '' or int(elt) < 1 or int(elt) > 9:
                return False
            # handle case where value is repeated
            if dict[elt] is not None:
                return False
            # handle case where value is unique
            dict[elt] = True
        # double check that all values were found
        for key in dict:
            if dict[key] is None:
                return False
    # all tests passed, return True
    return True