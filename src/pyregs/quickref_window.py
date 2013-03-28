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

from .widgets import PRTreeview

tree_data = [
    ('.', 'Match any character except a newline.'),
    ('^', 'Match the start of the string.'),
    ('$', 'Match the end of the string.'),
    ('*', 'Match 0 or more repetitions of the preceding RE.'),
    ('+', 'Match 1 or more repetitions of the preceding RE.'),
    ('?', 'Match 0 or 1 repetitions of the preceding RE.'),
    ('*?', 'Non-greedy "*"'),
    ('+?', 'Non-greedy "+"'),
    ('??', 'Non-greedy "?"'),
    ('{{m}}', 'Match exactly m copies of the previous RE.'),
    ('{{m,n}}', 'Match from m to n repetitions of the preceding RE.'),
    ('{{m,n}?}', 'Non-greedy {m,n}.'),
    ('\\ ', 'Escape special character or signal a special sequence.'),
    ('[]', 'Indicate a set of characters.'),
    ('A|B', 'Match either A or B.'),
    ('(...)', 'Match regex inside the parentheses, and indicate the start and'
              ' end of a group.'),
    ('(?:...)', 'A non-capturing version of regular parentheses.'),
    ('(?P<name>...)', 'Like (...) but substring is accessible within the regexp'
                      ' via the symbolic name <name>.'),
     ('(?P=name)', 'Match whatever text was matched by the earlier group named'
                   ' name.'),
     ('(?#...)', 'A comment; the contents of the parentheses are ignored.'),
     ('(?=...)', 'Matches if ... matches next, but doesn’t consume any of'
                 ' the string.'),
     ('(?!...)', 'Matches if ... doesn’t match next.'),
     ('(?<=...)', 'Matches if the current position in the string is preceded '
                  'by a match for ... that ends at the current position.'),
      ('(?<!...)', 'Matches if the current position in the string is not '
                   'preceded by a match for ...'),
    ('(?aiLmsux)', 'Set the corresponding flag.'),
    ]

class QuickReferenceWindow(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.title('PyRegs regular expressions quick reference')
        self.geometry('640x480')
        # NEXT FRAME
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True)
        tree_columns = ('regex', 'desc')

        ttk.Style().configure('BIG.Treeview', rowheight=40)
        tree = PRTreeview(frame, columns=tree_columns, show='headings', style='BIG.Treeview')
        tree.column('regex', width=100, anchor=tk.CENTER)
        tree.column('desc', width=540)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.heading('regex', text='RegEx')
        tree.heading('desc', text='Description')

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=1)

        for item in tree_data:
            tree.insert('', 'end', values=item)
