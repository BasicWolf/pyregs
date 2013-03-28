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

import types
import re

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

from .widgets import (PRText, PRSpinbox, PRReadonlyText,
                      PRStatusBar, PRTreeview, PRCheckbutton, Timer)
from .util import bind, log_except
from .quickref_window import QuickReferenceWindow
from .about_window import AboutWindow
from .tooltip import ToolTip
from . import analyzer


import logging
log = logging.getLogger(__name__)


ASCII_TOOLTIP=r"""Make \w, \W, \b, \B, \d, \D, \s and \S perform ASCII-only matching instead of full Unicode matching. This is only meaningful for Unicode patterns, and is ignored for byte patterns."""
IGNORECASE_TOOLTIP = """Perform case-insensitive matching; expressions like [A-Z] will match lowercase letters, too. This is not affected by the current locale and works for Unicode characters as expected."""
LOCALE_TOOLTIP = """Make \w, \W, \b, \B, \s and \S dependent on the current locale. The use of this flag is discouraged as the locale mechanism is very unreliable, and it only handles one “culture” at a time anyway; you should use Unicode matching instead, which is the default in Python 3 for Unicode (str) patterns."""
_DOTALL_TOOLTIP = """Make the '.' special character match any character at all,including a newline; without this flag, '.' will match anything except a newline."""
MULTILINTE_TOOLTIP = """When specified, the pattern character '^' matches at the beginning of the string and at the beginning of each line (immediately following each newline); and the pattern character '$' matches at the end of the string and at the end of each line (immediately preceding each newline). By default, '^' matches only at the beginning of the string, and '$' only at the end of the string and immediately before the newline (if any) at the end of the string."""
VERBOSE_TOOLTIP = """Whitespace within the pattern is ignored, except when in a character class or preceded by an unescaped backslash, and, when a line contains a '#' neither in a character class or preceded by an unescaped backslash, all characters from the leftmost such '#' through the end of the line are ignored."""

class MainWindow:
    ANALYZER_CHECK_PERIOD = 100

    def __init__(self, root):
        # self._previous_state = None
        # self._current_state = None
        self.root = root
        self.setup_analyzer()
        self.setup_font()
        self.setup_ui()

    def setup_analyzer(self):
        self.analyzer = analyzer.RegExAnalyzer()

    def setup_font(self):
        self.font = tkfont.Font(family='Helvetica', size=10)

    def setup_ui(self):
        FRAME_HEIGHT = 120
        FRAME_WIDTH = 240
        TEXT_WIDTH_CHARS = 80
        TEXT_HEIGHT_LINES = 7
        root = self.root
        root.title('PyRegs')
        master_frame = ttk.Frame(root)
        master_frame.pack()

        ttk_style = ttk.Style()
        ttk_style.configure('.', font=self.font)
        self._input_timer = Timer(root, 300, self.on_input_modified)

        #-- setup menu ---#
        #-----------------#
        menu = tk.Menu(tearoff=False, font=self.font)
        root.config(menu=menu)
        pr_menu = tk.Menu(menu, tearoff=False, font=self.font)
        menu.add_cascade(label='PyRegs', menu=pr_menu)
        pr_menu.add_command(label='Exit', command=root.quit)

        tools_menu = tk.Menu(menu, tearoff=False, font=self.font)
        menu.add_cascade(label='Tools', menu=tools_menu)
        tools_menu.add_command(label='Quick reference',
                               command=self.on_tools_library_menu)

        help_menu = tk.Menu(menu, tearoff=False, font=self.font)
        menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About',
                              command=self.on_help_about_menu)


        #--- setup pattern frame ---#
        #---------------------------#
        frame = tk.LabelFrame(
            master_frame,
            text='Regular expression pattern',
            bd=2,
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            relief=tk.GROOVE,
            font=self.font
        )
        frame.pack()

        self.pattern_tbox = PRText(
            frame,
            height=3,
            width=TEXT_WIDTH_CHARS,
            font=self.font,
        )
        self.pattern_tbox.pack()
        bind(self.pattern_tbox.on_modified, self._input_timer.restart)

        #--- setup the analyzed text frame ---#
        #-------------------------------------#
        frame = tk.LabelFrame(
            master_frame,
            text='Analyzed text',
            bd=2,
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            relief=tk.GROOVE,
            font=self.font
        )
        frame.pack()
        self.analyzed_tbox = PRText(
            frame,
            height=TEXT_HEIGHT_LINES,
            width=TEXT_WIDTH_CHARS,
            font=self.font,
        )
        self.analyzed_tbox.pack()
        bind(self.analyzed_tbox.on_modified, self._input_timer.restart)

        #--- setup results frame and notebook ---#
        #----------------------------------------#
        results_frame = tk.LabelFrame(
            master_frame,
            text='Results',
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            bd=2,
            relief=tk.GROOVE,
            font=self.font
        )

        results_frame.columnconfigure(0, weight=8)
        results_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(2, weight=1)

        results_frame.pack(fill=tk.X)
        lbl = ttk.Label(results_frame, wraplength='4i', justify=tk.LEFT, anchor=tk.N,
                        text='Match #:')
        lbl.grid(row=0, column=1, sticky=(tk.E,))
        match_spinbox = PRSpinbox(
            results_frame,
            from_=0,
            to=0,
            font=self.font
        )
        match_spinbox.grid(row=0, column=2, sticky=(tk.E,))
        match_spinbox.config(state='disabled')
        bind(match_spinbox.on_modified, self.on_match_spinbox_modified)
        self.match_spinbox = match_spinbox
        # setup notebook
        nb = ttk.Notebook(results_frame)
        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()
        # nb.pack(fill=tk.BOTH, expand=tk.Y, padx=2, pady=3)
        nb.grid(row=1, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame = ttk.Frame(nb)
        frame.pack()
        match_tbox = PRReadonlyText(
            frame,
            height=TEXT_HEIGHT_LINES,
            width=TEXT_WIDTH_CHARS,
            font=self.font,
        )
        match_tbox.tag_config('highlight', background='yellow')
        match_tbox.pack(expand=tk.Y, fill=tk.BOTH)
        self.match_tbox = match_tbox
        nb.add(frame, text='Match', underline=0, padding=2)

        # NEXT FRAME
        frame = ttk.Frame(nb)
        frame.pack(fill='both', expand=True)
        tree_columns = ('group', 'value')

        tree = PRTreeview(frame, columns=tree_columns, show="headings", height=5)
        vsb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.heading('group', text='Group')
        tree.heading('value', text='Value')

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=tk.Y)
        self.match_tree = tree
        nb.add(frame, text='Group', underline=0)

        # NEXT FRAME
        #----------
        frame = ttk.Frame(nb)
        # fframe = flags_frame
        fframe = tk.LabelFrame(frame, text='Flags', font=self.font)
        fframe.grid()
        # frame.rowconfigure(1, weight=1)
        # frame.columnconfigure((0,1), weight=1, uniform=0)
        def _make_tooltip(parent, text):
            ToolTip(parent,
                    wraplength=300,
                    font=self.font,
                    text=text)

        cb = PRCheckbutton(fframe, text='ASCII', font=self.font)
        cb.grid(row=0, column=0, sticky=tk.W)
        bind(cb.on_modified, self._input_timer.restart)
        _make_tooltip(cb, ASCII_TOOLTIP)
        self.ascii_cb = cb

        cb = PRCheckbutton(fframe, text='IGNORECASE', font=self.font)
        cb.grid(row=1, column=0, sticky=tk.W)
        bind(cb.on_modified, self._input_timer.restart)
        _make_tooltip(cb, IGNORECASE_TOOLTIP)
        self.ignorecase_cb = cb

        cb = PRCheckbutton(fframe, text='LOCALE', font=self.font)
        cb.grid(row=2, column=0, sticky=tk.W)
        bind(cb.on_modified, self._input_timer.restart)
        _make_tooltip(cb, LOCALE_TOOLTIP)
        self.locale_cb = cb

        cb = PRCheckbutton(fframe, text='MULTILINE', font=self.font)
        cb.grid(row=2, column=0, sticky=tk.W)
        bind(cb.on_modified, self._input_timer.restart)
        _make_tooltip(cb, MULTILINTE_TOOLTIP)
        self.multiline_cb = cb

        cb = PRCheckbutton(fframe, text='DOTALL', font=self.font)
        cb.grid(row=3, column=0, sticky=tk.W)
        bind(cb.on_modified, self._input_timer.restart)
        _make_tooltip(cb, _DOTALL_TOOLTIP)
        self.dotall_cb = cb

        cb = PRCheckbutton(fframe, text='VERBOSE', font=self.font)
        cb.grid(row=4, column=0, sticky=tk.W)
        bind(cb.on_modified, self._input_timer.restart)
        _make_tooltip(cb, VERBOSE_TOOLTIP)
        self.verbose_cb = cb

        nb.add(frame, text='Options', underline=0)

        # STATUS BAR #
        # ---------- #
        self.status_bar = PRStatusBar(master_frame, font=self.font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_input_modified(self):
        pattern_text = self.pattern_tbox.text
        analyzed_text = self.analyzed_tbox.text
        pattern_text = pattern_text.strip()
        analyzed_text = analyzed_text.strip()

        if pattern_text == '' or analyzed_text == '':
            self._clear_results()
            return

        flags = 0
        flags |= re.ASCII if self.ascii_cb.checked else 0
        flags |= re.IGNORECASE if self.ignorecase_cb.checked else 0
        flags |= re.LOCALE if self.locale_cb.checked else 0
        flags |= re.MULTILINE if self.multiline_cb.checked else 0
        flags |= re.DOTALL if self.dotall_cb.checked else 0
        flags |= re.VERBOSE if self.verbose_cb.checked else 0
        self._analyze(pattern_text, analyzed_text, flags)

    def _clear_results(self):
        self.match_spinbox.clear()
        self.match_spinbox.config(state=tk.DISABLED)
        self.match_tbox.clear()
        self.match_tree.clear()

    @log_except
    def _analyze(self, pattern_text, analyzed_text, flags=0):
        # configure widgets
        self.match_spinbox.config(state='disabled', from_=0, to=0)
        self.match_tbox.clear()
        self._previous_match_ind_start = None
        self._previous_match_ind_end = None
        self._previous_match_number = 1

        # restart analyzer
        self.analyzer.stop()
        self.analyzer = analyzer.RegExAnalyzer(pattern_text,
                                                analyzed_text,
                                                flags)
        self.analyzer.start()
        self.check_analyzer()

    @log_except
    def check_analyzer(self):
        anl = self.analyzer
        # RegExAnalayzer.state is a value from another thread.
        # Thus, we have to save it's state here once for the rest
        # of the routine in order to emulate swtich()-like construction.
        state = anl.state
        status = anl.status
        self.status_bar.text = status

        if state not in [analyzer.FINISHED_SUCCESS, analyzer.FINISHED_ERROR]:
            self.root.after(self.ANALYZER_CHECK_PERIOD, self.check_analyzer)
            return

        if state == analyzer.FINISHED_SUCCESS:
            # enable and setup the widgets
            if len(anl.matches) == 0:
                return

            self.match_tbox.text = anl.text
            self.match_spinbox.config(state='normal',
                                      from_=1,
                                      to=len(anl.matches))

            if (self._previous_match_number <= len(anl.matches)):
                self.match_spinbox.clear()
                self.match_spinbox.text = self._previous_match_number
        elif state == analyzer.FINISHED_ERROR:
            pass

    @log_except
    def on_match_spinbox_modified(self, value):
        try:
            match_id = int(value) - 1
        except ValueError:
            return
        mo = self.analyzer.matches[match_id]
        self.update_match_box(mo)
        self.update_tree_view(mo)

    def update_match_box(self, mo):
        index_start = '1.0+{} chars'.format(mo.start())
        index_end = '1.0+{} chars'.format(mo.end())
        # remove previous tag if any
        if self._previous_match_ind_start is not None:
            self.match_tbox.tag_remove('highlight',
                                       self._previous_match_ind_start,
                                       self._previous_match_ind_end)

        self.match_tbox.tag_add('highlight', index_start, index_end)
        self.match_tbox.mark_set(tk.INSERT, index_start)
        self.match_tbox.see(index_start)
        self._previous_match_ind_start = index_start
        self._previous_match_ind_end = index_end

    def update_tree_view(self, mo):
        self.match_tree.clear()

        anl = self.analyzer
        if anl.re_groups_count == 0:
            return

        i = 1
        groups = []
        for val in mo.groups():
            groups.append((i, val))
            i += 1

        # map named groups instead of group numbers
        for group_name, group_number in anl.re_groupindex.items():
            new_tuple = (group_name, groups[group_number - 1][1])
            groups[group_number - 1] = new_tuple

        for item in groups:
            self.match_tree.insert('', tk.END, values=item)

    def on_tools_library_menu(self):
        QuickReferenceWindow(self.root)

    def on_help_about_menu(self):
        AboutWindow(self.root)

    # def OnBigger(self):
    #     '''Make the font 2 points bigger'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size+2)

    # def OnSmaller(self):
    #     '''Make the font 2 points smaller'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size-2)
