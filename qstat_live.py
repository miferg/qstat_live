#! /usr/bin/python3

import curses
import sys
import subprocess

def main_menu(stdscr):

    k = 0
    cursor_x = 0
    cursor_y = 0

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while True:

        if k == ord('q'):
            sys.exit()

        # Initialization
        curses.curs_set(False)
        stdscr.nodelay(True)
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Call qstat
        process = subprocess.Popen('qstat', stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        qstat = str(stdout)[2:-1].split('\\n')[:-1]

        # Strings
        statusbarstr = " Miguel Romero 2020 | github.com/romeromig | press 'q' to exit "
        title = " qstat, {} jobs".format(len(qstat)-2)

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Rendering title
        stdscr.attron(curses.color_pair(3))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(0, 0, title)
        stdscr.addstr(0, len(title), " " * (width - len(title) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print the qstat report, line by line until the screen is filled
        for i in range(0, min(len(qstat),height-3)):
            stdscr.addstr(i+1, 0, qstat[i])

        # Refresh the screen
        stdscr.refresh()

        curses.napms(100)

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()

