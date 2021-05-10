import argparse
from itertools import product

def main():

    parser = argparse.ArgumentParser(description='simple sudoku solver program')

    parser.add_argument("Input", type=int, nargs="+" , help="input a starting configuration as a list 9x9 long, with 0 in empty cells, read left to right top to bottom")

    args = parser.parse_args()

    #print(args.Input)
    print(len(args.Input))

    size = 9
    grid = [[[n for n in range(1,10)] for x in range(size)] for u in range(size)]

    #
    for ((x,y),n) in zip(product(range(size), repeat=2), range(size**2)):
        if args.Input[n] != 0:
            grid[x][y] = [args.Input[n]]
        print(grid[x][y])


if __name__ == '__main__':
    main()