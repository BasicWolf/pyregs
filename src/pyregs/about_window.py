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

import tkinter as tk
import tkinter.ttk as ttk

ABOUT_TEXT = """
PyRegs is a small regular expressions debugger written by Zaur Nasibov

It was heavily inspired by another wonderful regex debugger, "Kodos"
which was unfortunately excluded from various GNU/Linux distros due
to the lack of PyQT3 surrort.

PyRegs is written in Python 3 and tkinter widgets which are by-default
shipped with Python and have out-of-the-box support on various platforms.

The program is distributed under the terms of GPLv3 license. We respect
every user's freedom to get under the hood of a product he or she is using
and a freedom to modify and distribute it, as long as the same freedom is
passed along.

For updates, questions, ideas, patches, contributions and personal please
visit me at http://znasibov.info or http://github.com/basicwolf
"""

class AboutWindow(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.title('About PyRegs')
        self.geometry('640x480')

        style = ttk.Style()
        style.configure('Wh.TFrame', background='white')
        style.configure('Wh.TLabel', background='white')
        style.configure('H1.TLabel', background='white',
                        font='Helvetica 14 bold')
        style.configure('Href.TLabel', background='white', foreground='blue',
                        font='Helvetica 12 underline')

        frame = ttk.Frame(self, style='Wh.TFrame')
        frame.pack(fill='both', expand=True)

        lbl = ttk.Label(frame, text='PyRegs v0.1', style='H1.TLabel')
        lbl.pack()
        lbl = ttk.Label(frame, wraplength=600, text=ABOUT_TEXT, style='Wh.TLabel')
        lbl.pack()
        close_button = ttk.Button(self, text="Close", command=self.destroy)
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
