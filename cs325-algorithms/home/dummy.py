from views import SudokuBoard
import heapq

def main():

    # for _ in range(20):
        # print('iteration')
    s = SudokuBoard(3)
    print('outer clues: ', 81 - len(s.empties))
    for row in s.grid:
        print(row)
        # print('grid: ')
        # for row in s.grid:
        #     print(row)
        # print('===================')
        # print('solved: ')
        # for row in s.solved:
        #     print(row)
        # print('==================')
    # for row in s.grid:
    #     print(row)
    # print('================')
    # print('rows: ')
    # for row in s.rows:
    #     print(row)
    # print('================')
    # print('cols: ')
    # for row in s.cols:
    #     print(row)
    # print('================')
    # print('sqs: ')
    # for row in s.squares:
    #     print(row)
    # print('================')
    # for i in range(9):
    #     for j in range(9):
    #         sq = (i // 3) * 3 + (j // 3)
    #         if not s.placement_is_valid(i, j, sq, s.grid[i][j]):


    # num_clues = []
    # for _ in range(50):
    #     s = SudokuBoard(3)
    #     heapq.heappush(num_clues, 81 - len(s.empties))
    #     print('clues: ', 81 - len(s.empties))
    #     for row in s.grid:
    #         print(row)
    #     print('================')
    # while num_clues:
    #     print(heapq.heappop(num_clues))




if __name__ == '__main__':
    main()