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
        for ((y,x),n) in zip(product(range(self.size), repeat=2), range(self.size**2)):
            if initialState[n] != 0:
                self.grid[x][y] = [initialState[n]]
            #print('('+str(x)+','+str(y)+') :' + str(self.grid[x][y]))

        #each square contains 'size' number of cells, 
        # there are 'size' number of squares in the whole puzzle
        self.subSidelength = math.isqrt(self.size)
        

    def solve(self):
        pass

    #recursively check all the constraints starting from cell (x,y)
    def make_consistent(self, x, y):
        n_modified = 0
        #check row and column
        for (m,n) in product(range(self.size),[y]):
            cell = self.grid[m][n]
            #print("checking: " + str(m) + ',' + str(n) + ": " + str(cell))
            if len(cell) == 1 and (cell[0] in self.grid[x][y]):
                print(cell)
                self.grid[x][y].remove(cell[0])
                #n_modified += self.make_consistent(m,n) + 1
                #print("modified: " + str(x) + ',' + str(y) + " - removed:" + str(cell[0]))

        print('('+str(x)+','+str(y)+') ' + "final domain after row check: " + str(self.grid[x][y]))

        for (m,n) in product([x], range(self.size)):
            pass

        #check square
        ##first calculate the starting index of the subsquare that (x,y) is in
        ##and then iterate over the whole square
        xStart = (x//self.subSidelength)*self.subSidelength
        yStart = (y//self.subSidelength)*self.subSidelength
        for (m,n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
            pass
        return n_modified

    def show(self):
        pass

def main():

    parser = argparse.ArgumentParser(description='simple sudoku solver program')

    parser.add_argument("Input", type=int, nargs="+" , help="input a starting configuration as a list 9x9 long, with 0 in empty cells, read left to right top to bottom")

    args = parser.parse_args()

    print(len(args.Input))

    sudoku = Sudoku(args.Input)

    #main arc consisitency checking loop
    
    sudoku.make_consistent(0,2)




if __name__ == '__main__':
    main()