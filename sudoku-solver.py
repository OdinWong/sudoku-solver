import argparse
import math
from itertools import product



class Sudoku():
    
    def __init__(self, initialState):
        #at this stage only allow 9x9 sudoku squares
        self.size = 9
        self.grid = [[[n for n in range(1,10)] for x in range(self.size)] for u in range(self.size)]

        #put input arguments into grid to initialize starting values,
        #only takes size^2 values from the inital state list provided
        #TODO check size/initialState is a valid size
        for ((x,y),n) in zip(product(range(self.size), repeat=2), range(self.size**2)):
            if initialState[n] != 0:
                self.grid[x][y] = [initialState[n]]
            #print('('+str(x)+','+str(y)+') :' + str(self.grid[x][y]))

        #each square contains 'size' number of cells, 
        # there are 'size' number of squares in the whole puzzle
        self.subSidelength = math.isqrt(self.size)
        

    #solve the sudoku,
    #run arc consistency algorithm, and if not solved try values with backtracking
    def solve(self):
    
        self.make_consistent()
        solved = True
        

        #find cell with least possible values
        min_len = self.size + 1
        min_index = ()
        for (x,y) in product(range(self.size), repeat=2):
            if len(self.grid[x][y]) > 1:
                #found unsolved cell
                solved = False
                #look for cell with minimum remaining values
                if len(self.grid[x][y]) <= min_len:
                    min_len = len(self.grid[x][y])
                    min_index = (x,y)
        
        return solved
        if not solved:
            cell = self.grid[min_index[0]][min_index[1]].copy()
            for val in cell:
                #try value
                self.grid[min_index[0]][min_index[1]] = [val]
                solved = self.solve()
                if solved:
                    return True
                #reset
            self.grid[min_index[0]][min_index[1]] = cell.copy()

        return solved


    #makes all arcs locally consistent
    def make_consistent(self):
        for (x,y) in product(range(self.size), repeat=2):
            self.make_locally_consistent(x,y)


    #make the arcs from a cell (x,y) locally consistent, by removing values from the relevant cells
    #called recursively on any cells that are restricted to only a single value
    def make_locally_consistent(self, x, y):
        n_modified = 0
        if len(self.grid[x][y]) != 1:
            return 0

        #check row and column
        for (m,n) in product(range(self.size),[y]):
            #skip self-check
            if x==m and y == n:
                continue
            self.__check_local_arc__(x,y,m,n)

        for (m,n) in product([x], range(self.size)):
            #skip self-check
            if x==m and y == n:
                continue
            self.__check_local_arc__(x,y,m,n)

        #check square
        ##first calculate the starting index of the subsquare that (x,y) is in
        ##and then iterate over the whole square
        xStart = (x//self.subSidelength)*self.subSidelength
        yStart = (y//self.subSidelength)*self.subSidelength
        for (m,n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
             #skip self-check
            if x==m and y == n:
                continue
            self.__check_local_arc__(x,y,m,n)


    #helper for checking one arc
    def __check_local_arc__(self, x,y,m,n):
        cell = self.grid[m][n]

        if len(self.grid[x][y]) == 0:
            return False

        locked_value = self.grid[x][y][0]
        if (locked_value in cell):
            cell.remove(locked_value)
            self.make_locally_consistent(m,n)
        

    def show(self):
        for column in self.grid:
            for cell in column:
                if len(cell) == 1:
                    print(cell, end=' ')
                else:
                    print('[ ]', end=' ')
            print('')

def main():

    parser = argparse.ArgumentParser(description='simple sudoku solver program')

    parser.add_argument("Input", type=int, nargs="+" , help="input a starting configuration as a list 9x9 long, with 0 in empty cells, read left to right top to bottom")

    args = parser.parse_args()

    print(len(args.Input))

    sudoku = Sudoku(args.Input)

    #main arc consisitency checking loop
    sudoku.show()
    print('-------------------------')
    sudoku.make_consistent()
    sudoku.show()
    print('-------------------------')
    sudoku.solve()
    sudoku.show()




if __name__ == '__main__':
    main()