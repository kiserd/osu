from views import SudokuBoard

def main():
    s = SudokuBoard(3)
    # s.gen_solved_board()
    for row in s.board:
        print(row)





if __name__ == '__main__':
    main()