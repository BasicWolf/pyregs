#!/usr/bin/env python3
# Copyright (C) 2013 by Zaur Nasibov.
#
# This file is part of PyRegs.
#
# PyRegs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyRegs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyRegs.  If not, see <http://www.gnu.org/licenses/>.

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
