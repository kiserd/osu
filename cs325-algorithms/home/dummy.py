from views import SudokuBoard
import heapq

def main():
    num_clues = []
    for _ in range(50):
        s = SudokuBoard(3)
        heapq.heappush(num_clues, 81 - len(s.empties))
    while num_clues:
        print(heapq.heappop(num_clues))




if __name__ == '__main__':
    main()