import argparse
from itertools import product



class Sudoku():
    
    def __init__(self, initialState, size=9):
        self.size = size
        self.grid = [[[n for n in range(1,10)] for x in range(size)] for u in range(size)]

        #put input arguments into grid to initialize starting values
        for ((x,y),n) in zip(product(range(size), repeat=2), range(size**2)):
            if initialState[n] != 0:
                self.grid[x][y] = [initialState[n]]
            print(self.grid[x][y])

        

    def solve(self):
        pass

    #recursively check all the constraints starting from cell (x,y)
    def make_consistent(grid, x, y):
        #check row and column
        for (m,n) in product(range(size),[y]):
            pass

        for (m,n) in product([x], range(9)):
            pass

        #check square
        for (m,n) in product(range()):

    def show(self):
        pass

def main():

    parser = argparse.ArgumentParser(description='simple sudoku solver program')

    parser.add_argument("Input", type=int, nargs="+" , help="input a starting configuration as a list 9x9 long, with 0 in empty cells, read left to right top to bottom")

    args = parser.parse_args()

    print(len(args.Input))

    #main arc consisitency checking loop



if __name__ == '__main__':
    main()