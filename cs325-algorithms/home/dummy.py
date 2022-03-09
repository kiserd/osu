from views import SudokuBoard

def main():
    s = SudokuBoard(3)
    # s.gen_solved_board()
    for row in s.solved:
        print(row)
    print('=================')
    for row in s.grid:
        print(row)




if __name__ == '__main__':
    main()