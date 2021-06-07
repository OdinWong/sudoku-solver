import curses
from sudoku_solver import Sudoku

def main(scr):
    scr = curses.initscr()
    scr.clear()

    sudoku_box = scr.derwin(17,17, 1, 1)
    sudoku_box.box()

    for x in range(1,16):
        for y in range(1,16):
            if y%4==0 and x%4==0:
                sudoku_box.addch(y,x,ord('+'))
            elif y%4 == 0:
                sudoku_box.addch(y,x,ord('-'))
            elif x%4 == 0:
                sudoku_box.addch(y,x,ord('|'))

    sudoku_box.move(1,1)
    sudoku_box.keypad(1)

    key = None
    while True:
        key = sudoku_box.getch()
        cy,cx = sudoku_box.getyx()

        if key == curses.KEY_RIGHT:
            cx += 1
            if on_border(sudoku_box,cy,cx):
                continue
            elif not valid_position(cy,cx):
                cx += 1
        elif key == curses.KEY_LEFT:
            cx -= 1
            if on_border(sudoku_box,cy,cx):
                continue
            elif not valid_position(cy,cx):
                cx -= 1
        elif key == curses.KEY_UP:
            cy -= 1
            if on_border(sudoku_box,cy,cx):
                continue
            elif not valid_position(cy,cx):
                cy -= 1
        elif key == curses.KEY_DOWN:
            cy += 1
            if on_border(sudoku_box,cy,cx):
                continue
            elif not valid_position(cy,cx):
                cy += 1
        elif key == ord('q'):
            quit()

        sudoku_box.move(cy,cx)

def valid_position(y,x):
    if x%4 == 0 or y%4==0:
        return False
    return True

def on_border(scr,y,x):
    my,mx = scr.getmaxyx()

    if y == 0 or x == 0 or x >= mx - 1 or y >= my - 1:
        return True
    return False


if __name__ == '__main__':
    curses.wrapper(main)