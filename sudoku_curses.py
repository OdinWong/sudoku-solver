import curses
import curses.ascii
import sys

from sudoku_solver import Sudoku
from curses_menu import CursesMenu


def main(scr):
    scr = curses.initscr()
    scr.clear()

    sudoku_box = scr.derwin(13, 13, 1, 1)
    sudoku_box.box()

    sudoku = Sudoku()

    # setup grid in the sudoku window
    for x in range(1, 12):
        for y in range(1, 12):
            if y % 4 == 0 and x % 4 == 0:
                sudoku_box.addch(y, x, ord('+'), curses.A_BOLD)
            elif y % 4 == 0:
                sudoku_box.addch(y, x, ord('-'), curses.A_BOLD)
            elif x % 4 == 0:
                sudoku_box.addch(y, x, ord('|'), curses.A_BOLD)
    sudoku_box.refresh()

    # setup menu
    sby, sbx = sudoku_box.getmaxyx()

    menu = CursesMenu(scr, sby + 1, 0, 10, 20)

    #add menu items
    menu.add_item("edit sudoku", lambda a, i : edit_mode(sudoku_box, sudoku))
    menu.add_item("solve",lambda a, i : solve_sudoku(sudoku_box, sudoku))
    menu.add_item("update state", lambda a, i : update_sudoku_box(sudoku_box, sudoku))

    # main control loop
    menu.start_menu()

def solve_sudoku(sudoku_box, sudoku):
    #solve the sudoku
    sudoku.solve()
    update_sudoku_box(sudoku_box, sudoku)

def update_sudoku_box(sudoku_box, sudoku):
    #get data and update screen
    #flatten out list of cells
    cells = [cell for col in sudoku.get_state() for cell in col]
    index = 0
    for x in range(1,12):
        for y in range(1,12):
            if not (x % 4 == 0 or y % 4 == 0):
                if len(cells[index]) == 1:
                    sudoku_box.addch(y,x, str(cells[index][0]))
                else:
                    sudoku_box.addch(y,x, ord(' '))
                index += 1
    sudoku_box.refresh()


def edit_mode(sudoku_box, sudoku):
    sudoku_box.move(1, 1)
    sudoku_box.keypad(1)

    key = None
    while True:
        key = sudoku_box.getch()
        cy, cx = sudoku_box.getyx()

        if key == curses.KEY_RIGHT:
            cx += 1
            if on_border(sudoku_box, cy, cx):
                continue
            elif not valid_position(cy, cx):
                cx += 1
        elif key == curses.KEY_LEFT:
            cx -= 1
            if on_border(sudoku_box, cy, cx):
                continue
            elif not valid_position(cy, cx):
                cx -= 1
        elif key == curses.KEY_UP:
            cy -= 1
            if on_border(sudoku_box, cy, cx):
                continue
            elif not valid_position(cy, cx):
                cy -= 1
        elif key == curses.KEY_DOWN:
            cy += 1
            if on_border(sudoku_box, cy, cx):
                continue
            elif not valid_position(cy, cx):
                cy += 1
        elif key == ord('q'):
            return
        elif curses.ascii.isdigit(key) and key != ord('0'):
            #sudoku_box.addch(key)
            sudoku.edit_cell(cx - cx//4 - 1, cy - cy//4 - 1, int(chr(key)))
            update_sudoku_box(sudoku_box, sudoku)
        elif key == curses.KEY_BACKSPACE or key == ord('0'):
            sudoku_box.addch(' ')
            sudoku.edit_cell(cx - cx//4 - 1, cy - cy//4 - 1, None)

        sudoku_box.move(cy, cx)


def valid_position(y, x):
    if x % 4 == 0 or y % 4 == 0:
        return False
    return True


def on_border(scr, y, x):
    my, mx = scr.getmaxyx()

    if y == 0 or x == 0 or x >= mx - 1 or y >= my - 1:
        return True
    return False


if __name__ == '__main__':
    curses.wrapper(main)
