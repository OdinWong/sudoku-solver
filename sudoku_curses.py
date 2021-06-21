import curses
import curses.ascii
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
    screenmaxy, screenmaxx = scr.getmaxyx()

    menu = CursesMenu(scr, sby + 1, 0, 10, 20)

    menu.add_item("edit sudoku", lambda a, i : edit_mode(sudoku_box, sudoku))

    # main control loop
    menu.start_menu()


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
            sudoku_box.addch(key)
            sudoku.edit_cell(cx, cy, int(key))
        elif key == curses.KEY_BACKSPACE or key == ord('0'):
            sudoku_box.addch(' ')
            sudoku.edit_cell(cx, cy, 0)

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
