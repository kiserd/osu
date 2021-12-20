from django.shortcuts import render
from django.http import HttpResponse

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