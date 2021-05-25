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
        

    def solve(self):
    
        for (y,x) in product(range(self.size), repeat=2):
            self.make_consistent(x,y)


    #as for local consistency, only cells with a single possible value affect others, only propagate from these
    #checks and recursively propagates those that are restricted to a single value in the same way
    def make_consistent(self, x, y):
        n_modified = 0
        if len(self.grid[x][y]) != 1:
            return 0

        #check row and column
        for (m,n) in product(range(self.size),[y]):

            #skip self-check
            if x==m and y == n:
                continue

            cell = self.grid[m][n]
            locked_value = self.grid[x][y][0]
            #print("checking: " + str(m) + ',' + str(n) + ": " + str(cell))
            if (locked_value in cell):
                cell.remove(locked_value)
                n_modified += self.make_consistent(m,n) + 1
                #print("modified: " + str(m) + ',' + str(n) + " - removed:" + str(locked_value))

        #print("number of row cells modified: " + str(n_modified))

        for (m,n) in product([x], range(self.size)):
            #skip self-check
            if x==m and y == n:
                continue

            cell = self.grid[m][n]
            locked_value = self.grid[x][y][0]
            #print("checking: " + str(m) + ',' + str(n) + ": " + str(cell))
            if (locked_value in cell):
                cell.remove(locked_value)
                n_modified += self.make_consistent(m,n) + 1
                #print("modified: " + str(m) + ',' + str(n) + " - removed:" + str(locked_value))
        #print("number of column cells modified: " + str(n_modified))


        #check square
        ##first calculate the starting index of the subsquare that (x,y) is in
        ##and then iterate over the whole square
        xStart = (x//self.subSidelength)*self.subSidelength
        yStart = (y//self.subSidelength)*self.subSidelength
        for (m,n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
             #skip self-check
            if x==m and y == n:
                continue

            cell = self.grid[m][n]
            locked_value = self.grid[x][y][0]
            #print("checking: " + str(m) + ',' + str(n) + ": " + str(cell))
            if (locked_value in cell):
                cell.remove(locked_value)
                n_modified += self.make_consistent(m,n) + 1

        return n_modified

    def show(self):
        for column in self.grid:
            for cell in column:
                print(cell, end=' ')
            print('')

def main():

    parser = argparse.ArgumentParser(description='simple sudoku solver program')

    parser.add_argument("Input", type=int, nargs="+" , help="input a starting configuration as a list 9x9 long, with 0 in empty cells, read left to right top to bottom")

    args = parser.parse_args()

    print(len(args.Input))

    sudoku = Sudoku(args.Input)

    #main arc consisitency checking loop
    
    sudoku.solve()
    sudoku.show()




if __name__ == '__main__':
    main()