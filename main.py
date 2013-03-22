#!/usr/bin/env python3
import sys
import logging
import tkinter as tk
from pyregs import MainWindow


def main():
    setup_logging()
    root = tk.Tk()
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)
    main_form = MainWindow(root)
    root.mainloop()


def setup_logging():
    console_format = '%(levelname)-8s %(message)s'
    loglevel = logging.ERROR

    if '--debug' in sys.argv:
        loglevel = logging.DEBUG
        # add module in debug mode
        console_format += ' (%(name)s)'

    # Logging to terminal
    logging.basicConfig(level = loglevel,
                        format = console_format,
                        datefmt='%H:%M:%S',)


if __name__ == '__main__':
    main()
