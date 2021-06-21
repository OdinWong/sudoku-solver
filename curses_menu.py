# basic python curses menu class

import curses
import sys

class MenuItem():

    def __init__(self, text: str, id: int, on_activate):
        self._on_activate = on_activate
        self._id = id
        self.text = text

    def activate(self):
        self._on_activate(self.text, self._id)


class CursesMenu():

    def __init__(self, parent_screen, y: int, x: int, height: int, width: int, quit_item: bool = True):
        # list of menu items
        self.menu_items = []
        self.menuscreen = parent_screen.derwin(height, width, y, x)

        if quit_item:
            self.add_item("quit", lambda s,i : sys.exit())

    def add_item(self, text: str, on_activate):
        maxy, _ = self.menuscreen.getmaxyx()
        if len(self.menu_items) >= maxy:
            return False
        self.menu_items.append(
            MenuItem(text, len(self.menu_items), on_activate)
        )
        return True
    
    def _quit(s: str, i: int):
        quit()

    def add_toggle_item(self, text: str, on_activate, defaultstate: bool = True):
        pass

    def start_menu(self):

        # draw menu
        for index, item in enumerate(self.menu_items):
            maxy, _ = self.menuscreen.getmaxyx()

            if index < maxy:
                self.menuscreen.addstr(index, 0, item.text)

        # reset cursor
        self.menuscreen.move(0, 0)

        # main menu control loop
        index, _ = self.menuscreen.getyx()
        self.menuscreen.keypad(1)
        while True:
            key = self.menuscreen.getch()
            self.menuscreen.addstr(index, 0, self.menu_items[index].text)


            if key == curses.KEY_UP:
                if index != 0:
                    index -= 1
            elif key == curses.KEY_DOWN:
                if index != (len(self.menu_items) - 1):
                    index += 1
            elif key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r'):
                self.menu_items[index].activate()

            #highlight current item
            self.menuscreen.addstr(
                index,
                0,
                self.menu_items[index].text,
                curses.A_REVERSE
            )

            self.menuscreen.refresh()
