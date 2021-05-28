import argparse
import math
from itertools import product



class Sudoku():
    
    def __init__(self, initialState):
        #at this stage only allow 9x9 sudoku squares
        self.size = 9
        self.grid = [[[n for n in range(1,10)] for x in range(self.size)] for u in range(self.size)]

        #second grid to allow locking of values
        self.locked = [([False]*self.size) for u in range(self.size)]

        #put input arguments into grid to initialize starting values,
        #only takes size^2 values from the inital state list provided
        #TODO check size/initialState is a valid size
        for ((x,y),n) in zip(product(range(self.size), repeat=2), range(self.size**2)):
            if initialState[n] != 0:
                self.grid[x][y] = [initialState[n]]
                self.locked[x][y] = True

        #each square contains 'size' number of cells, 
        # there are 'size' number of squares in the whole puzzle
        self.subSidelength = math.isqrt(self.size)
        

    #solve the sudoku,
    #run arc consistency algorithm, and if not solved try values with backtracking
    def solve(self):
    
        solved = True

        #main arc consistency checking loop
        for (x,y) in product(range(self.size), repeat=2):
            self.make_consistent(x,y)
        

        return solved
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

    #make consistent, with recursive checks 
    #returns false if invalid state reached
    def make_consistent(self,x,y):
        if self.locked[x][y]:
            return True

        recheck = False
        possible_values = self.check_possible(x,y)

        #no possible values remaining = invalid state, abort and return false
        if possible_values == []:
            return False

        #if changing values, need to recheck
        if set(self.grid[x][y]) != set(possible_values):
            self.grid[x][y] = possible_values
            recheck = True

        #check if any values are unique in the row, col or subsquare
        unique_values = self.check_unique(x,y)
        
        if len(unique_values) > 1:
            #more than one unique value in this cell = invalid state, abort and return false
            return False
        elif len(unique_values) == 1:
            #a value is unique, must be placed here, then need to recheck
            self.grid[x][y] = unique_values
            recheck = True

        if recheck:
            #if changes made to this cell, recheck relevant other cells in row, column and subsquare
            #sets used to reduce redundant rechecks
            row = {r for r in product(range(self.size), [y])}
            row.remove((x,y))
            col = {r for r in product([x], range(self.size))}
            col.remove((x,y))

            xStart = (x//self.subSidelength)*self.subSidelength
            yStart = (y//self.subSidelength)*self.subSidelength
            square = {r for r in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength))}
            square.remove((x,y))

            for (m,n) in (row | col | square):
                valid = self.make_consistent(m,n)
                if not valid:
                    return False

        return True


    def check_possible(self,x,y):
        possible = [n for n in range(1,10)]

        #check row and column
        for (m,n) in product(range(self.size),[y]):
            #skip self-check
            if x==m and y == n:
                continue    
            if len(self.grid[m][n]) == 1 and (self.grid[m][n][0] in possible):
                possible.remove(self.grid[m][n][0])
            
        for (m,n) in product([x], range(self.size)):
            #skip self-check
            if x==m and y == n:
                continue
            if len(self.grid[m][n]) == 1 and (self.grid[m][n][0] in possible):
                possible.remove(self.grid[m][n][0])   

        #check square
        ##first calculate the starting index of the subsquare that (x,y) is in
        ##and then iterate over the whole square
        xStart = (x//self.subSidelength)*self.subSidelength
        yStart = (y//self.subSidelength)*self.subSidelength
        for (m,n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
             #skip self-check
            if x==m and y == n:
                continue
            if len(self.grid[m][n]) == 1 and (self.grid[m][n][0] in possible):
                possible.remove(self.grid[m][n][0])
        
        return possible

    def check_unique(self,x,y):
        unique = set()
        found = False

        #check to see if any value in the cell is unique in the row, col or subsquare
        for val in self.grid[x][y]:
            found = False

            #check row
            for (m,n) in product(range(self.size),[y]):
                #skip self-check
                if x==m and y == n:
                    continue
                if val in self.grid[m][n]:
                    #found the value -> not unique in row
                    found = True
                    break
            
            if not found:
                unique.add(val)
            found = False

            #check column
            for (m,n) in product([x], range(self.size)):
                #skip self-check
                if x==m and y == n:
                    continue
                if val in self.grid[m][n]:
                    #found the value -> not unique in col
                    found = True
                    break 

            if not found:
                unique.add(val)
            found = False

            #check square
            ##first calculate the starting index of the subsquare that (x,y) is in
            ##and then iterate over the whole square
            xStart = (x//self.subSidelength)*self.subSidelength
            yStart = (y//self.subSidelength)*self.subSidelength
            for (m,n) in product(range(xStart, xStart+self.subSidelength), range(yStart, yStart+self.subSidelength)):
                #skip self-check
                if x==m and y == n:
                    continue
                if val in self.grid[m][n]:
                    #found the value -> not unique in subsquare
                    found = True
                    break
            
            if not found:
                unique.add(val)
            found = False
            
            return list(unique)


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


    sudoku.solve()
    sudoku.show()




if __name__ == '__main__':
    main()