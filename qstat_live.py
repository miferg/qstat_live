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

    # Set mode
    switch = 0

    # Loop where k is the last character pressed
    while True:

        if k == ord('q'):
            sys.exit()

        # Respond if the switch was pressed
        if k == ord('.'):
            if switch == 0:
                switch = 1
            else:
                switch = 0
            k = -1

        # Initialization
        curses.curs_set(False)
        stdscr.nodelay(True)
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Call qstat
        if switch == 0:
            process = subprocess.Popen("qstat -u '*'", stdout=subprocess.PIPE, shell=True)
        else:
            process = subprocess.Popen('qstat', stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        qstat = str(stdout)[2:-1].split('\\n')[:-1]

        # Strings
        statusbarstr = " github.com/miferg | '.' to toggle all or user | 'q' to exit "
        if switch == 0:
            title = " qstat all users, {} jobs".format(len(qstat)-2)
            title_empty = " qstat all users, no jobs"
        if switch == 1:
            title = " qstat current user, {} jobs".format(len(qstat)-2)
            title_empty = " qstat current user, no jobs"

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
        if len(qstat)-2 == -2:
            stdscr.addstr(0, 0, title_empty)
            stdscr.addstr(0, len(title_empty), " " * (width - len(title) - 1))
        else:
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

