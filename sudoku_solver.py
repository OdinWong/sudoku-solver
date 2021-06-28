import argparse
import math
import copy
import sys
from itertools import product


class Sudoku():

    def __init__(self, initialState):
        # at this stage only allow 9x9 sudoku squares
        self.size = 9
        self.grid = [[[n for n in range(1, 10)] for x in range(
            self.size)] for u in range(self.size)]

        # put input arguments into grid to initialize starting values,
        # only takes size^2 values from the inital state list provided
        # TODO check size/initialState is a valid size
        for ((x, y), n) in zip(product(range(self.size), repeat=2), range(self.size**2)):
            if initialState[n] != 0:
                self.grid[x][y] = [initialState[n]]
            #print('('+str(x)+','+str(y)+') :' + str(self.grid[x][y]))

        # each square contains 'size' number of cells,
        # there are 'size' number of squares in the whole puzzle
        self.subSidelength = math.isqrt(self.size)

    def __init__(self):
        self.size = 9
        self.grid = [[[n for n in range(1, 10)] for x in range(
            self.size)] for u in range(self.size)]

        self.subSidelength = math.isqrt(self.size)


    # edit/input a number into a cell without any other checks, 0 or None resets the cell
    def edit_cell(self, x, y, num):
        if isinstance(num, str):
            num = int(num)

        if num == None or num == 0:
            # reset square
            self.grid[x][y] = [n for n in range(1, 10)]
        elif num > 0 and num <= 9:
            self.grid[x][y] = [num]


    #returns the value from a specific cell
    def get_cell(self, x, y):
        return self.grid[x][y].copy()

    #returns a deep copy of the full state of the sudoku
    def get_state(self):
        return copy.deepcopy(self.grid)

    # solve the sudoku,
    # run arc consistency algorithm, and if not solved try remaining values with backtracking
    def solve(self):
        self.make_consistent()
        self.backtracking()

    def backtracking(self):
        solved = True

        for (x, y) in product(range(self.size), repeat=2):
            if len(self.grid[x][y]) > 1:
                solved = False
                cell = self.grid[x][y].copy()
                for val in cell:
                    # try value
                    if self.__check_valid__(x, y, val):
                        self.grid[x][y] = [val]
                        solved = self.backtracking()
                        if solved:
                            return True
                        # reset
                        self.grid[x][y] = cell.copy()
                return solved
        return solved

    def __check_valid__(self, x, y, val):

        # check row and column
        for n in range(self.size):
            # skip self-check
            if y == n:
                continue
            if len(self.grid[x][n]) == 1 and val == self.grid[x][n][0]:
                return False

        for n in range(self.size):
            # skip self-check
            if x == n:
                continue
            if len(self.grid[n][y]) == 1 and val == self.grid[n][y][0]:
                return False

        # check square
        # first calculate the starting index of the subsquare that (x,y) is in
        # and then iterate over the whole square
        xStart = (x//self.subSidelength)*self.subSidelength
        yStart = (y//self.subSidelength)*self.subSidelength
        for (m, n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
            # skip self-check
            if x == m and y == n:
                continue
            if len(self.grid[m][n]) == 1 and val == self.grid[m][n][0]:
                return False
        return True

    # makes all arcs locally consistent
    def make_consistent(self):
        for (x, y) in product(range(self.size), repeat=2):
            self.make_locally_consistent(x, y)

    # make the arcs from a cell (x,y) locally consistent, by removing values from the relevant cells
    # called recursively on any cells that are restricted to only a single value

    def make_locally_consistent(self, x, y):
        n_modified = 0
        if len(self.grid[x][y]) != 1:
            return 0

        # check row and column
        for (m, n) in product(range(self.size), [y]):
            # skip self-check
            if x == m and y == n:
                continue
            self.__check_local_arc__(x, y, m, n)

        for (m, n) in product([x], range(self.size)):
            # skip self-check
            if x == m and y == n:
                continue
            self.__check_local_arc__(x, y, m, n)

        # check square
        # first calculate the starting index of the subsquare that (x,y) is in
        # and then iterate over the whole square
        xStart = (x//self.subSidelength)*self.subSidelength
        yStart = (y//self.subSidelength)*self.subSidelength
        for (m, n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
            # skip self-check
            if x == m and y == n:
                continue
            self.__check_local_arc__(x, y, m, n)

    # helper for checking one arc
    def __check_local_arc__(self, x, y, m, n):
        cell = self.grid[m][n]

        if len(self.grid[x][y]) == 0:
            return False

        locked_value = self.grid[x][y][0]
        if (locked_value in cell):
            cell.remove(locked_value)
            self.make_locally_consistent(m, n)

    def show(self):
        for column in self.grid:
            for cell in column:
                if len(cell) == 1:
                    print(cell, end=' ')
                else:
                    print('[ ]', end=' ')
            print('')


def main():

    parser = argparse.ArgumentParser(
        description='simple sudoku solver program')

    parser.add_argument("Input", type=int, nargs="+",
                        help="input a starting configuration as a list 9x9 long, with 0 in empty cells, read left to right top to bottom")

    args = parser.parse_args()

    print(len(args.Input))

    sudoku = Sudoku(args.Input)

    # main arc consisitency checking loop
    sudoku.show()
    print('-------------------------')
    sudoku.make_consistent()
    sudoku.show()
    print('-------------------------')
    sudoku.solve()
    sudoku.show()


if __name__ == '__main__':
    main()
