import types
import re

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk

from .widgets import (PRText, PRSpinbox, PRReadonlyText,
                      PRStatusBar, PRTreeview, Timer)
from .util import bind, log_except
from .tooltip import ToolTip
from . import analyzer

import logging
log = logging.getLogger(__name__)

class MainWindow:
    ANALYZER_CHECK_PERIOD = 100

    def __init__(self, root):
        # self._previous_state = None
        # self._current_state = None
        self._root = root
        self._setup_analyzer()
        self._setup_font()
        self._setup_ui()

    def _setup_analyzer(self):
        self._analyzer = analyzer.RegExAnalyzer()

    def _setup_font(self):
        self._font = tkfont.Font(family="Helvetica", size=11)

    def _setup_ui(self):
        FRAME_HEIGHT = 120
        FRAME_WIDTH = 240
        TEXT_WIDTH_CHARS = 80
        TEXT_HEIGHT_LINES = 7
        root = self._root
        self._input_timer = Timer(root, 300, self._on_input_modified)
        root.title('PyRegs')
        master_frame = ttk.Frame(root)
        master_frame.pack()


        #--- setup pattern frame ---#
        #---------------------------#
        frame = tk.LabelFrame(
            master_frame,
            text='Regular expression pattern',
            bd=2,
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            relief=tk.GROOVE,
            font=self._font
        )
        frame.pack()

        self.pattern_tbox = PRText(
            frame,
            height=TEXT_HEIGHT_LINES,
            width=TEXT_WIDTH_CHARS
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
            font=self._font
        )
        frame.pack()
        self.analyzed_tbox = PRText(
            frame,
            height=TEXT_HEIGHT_LINES,
            width=TEXT_WIDTH_CHARS
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
            font=self._font
        )

        results_frame.columnconfigure(0, weight=8)
        results_frame.columnconfigure(1, weight=1)
        results_frame.columnconfigure(2, weight=1)

        results_frame.pack(fill=tk.X)
        lbl = ttk.Label(results_frame, wraplength='4i', justify=tk.LEFT, anchor=tk.N,
                        text='Match #:')
        lbl.grid(row=0, column=1, sticky=(tk.E,))
        match_spinbox = PRSpinbox(results_frame, from_=0, to=0)
        match_spinbox.grid(row=0, column=2, sticky=(tk.E,))
        match_spinbox.config(state='disabled')
        bind(match_spinbox.on_modified, self._on_match_spinbox_modified)
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
            width=TEXT_WIDTH_CHARS
        )
        match_tbox.tag_config('highlight', background='yellow')
        match_tbox.pack(expand=1, fill=tk.BOTH)
        self.match_tbox = match_tbox
        nb.add(frame, text='Match', underline=0, padding=2)

        # NEXT FRAME
        frame = ttk.Frame(nb)
        frame.pack(fill='both', expand=True)
        tree_columns = ('Group', 'Value')

        tree = PRTreeview(columns=tree_columns, show="headings", height=5)
        vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        for col in ('Group', 'Value'):
            tree.heading(col, text=col.title())

        tree.grid(column=0, row=0, sticky='nsew', in_=frame)
        self.match_tree = tree
        vsb.grid(column=1, row=0, sticky='ns', in_=frame)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        nb.add(frame, text='Group')

        # NEXT FRAME
        #----------
        frame = ttk.Frame(nb)
        # fframe = flags_frame
        fframe = tk.LabelFrame(frame, text='Flags')
        fframe.grid()
        # frame.rowconfigure(1, weight=1)
        # frame.columnconfigure((0,1), weight=1, uniform=0)

        cb = tk.Checkbutton(fframe, text='ASCII')
        cb.grid(row=0, column=0, sticky=tk.W)
        cb = tk.Checkbutton(fframe, text='IGNORECASE')
        cb.grid(row=1, column=0, sticky=tk.W)
        cb = tk.Checkbutton(fframe, text='LOCALE')
        cb.grid(row=2, column=0, sticky=tk.W)
        cb = tk.Checkbutton(fframe, text='MULTILINE')
        cb.grid(row=2, column=0, sticky=tk.W)
        cb = tk.Checkbutton(fframe, text='DOTALL')
        cb.grid(row=3, column=0, sticky=tk.W)
        cb = tk.Checkbutton(fframe, text='VERBOSE')
        cb.grid(row=4, column=0, sticky=tk.W)
        ToolTip(cb,
                wraplength=300,
                text=("Whitespace within the pattern is ignored, except"
                      "when in a character class or preceded by an"
                      "unescaped backslash, and, when a line contains "
                      "a '#' neither in a character class or preceded by "
                      "an unescaped backslash, all characters from the "
                      "leftmost such '#' through the end of the line are "
                      "ignored."))
        # add to notebook (underline = index for short-cut character)
        nb.add(frame, text='Options')

        # STATUS BAR #
        # ---------- #
        self.status_bar = PRStatusBar(master_frame)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_input_modified(self):
        pattern_text = self.pattern_tbox.text
        analyzed_text = self.analyzed_tbox.text
        pattern_text = pattern_text.strip()
        analyzed_text = analyzed_text.strip()

        if pattern_text == '' or analyzed_text == '':
            self._clear_results()
            return

        self._analyze(pattern_text, analyzed_text)

    def _clear_results(self):
        self.match_spinbox.clear()
        self.match_spinbox.config(state='disabled')
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
        self._analyzer.stop()
        self._analyzer = analyzer.RegExAnalyzer(pattern_text,
                                                analyzed_text,
                                                flags)
        self._analyzer.start()
        self._check_analyzer()

    @log_except
    def _check_analyzer(self):
        anl = self._analyzer
        # RegExAnalayzer.state is a value from another thread.
        # Thus, we have to save it's state here once for the rest
        # of the routine in order to emulate swtich()-like construction.
        state = anl.state
        status = anl.status
        self.status_bar.text = status

        if state not in [analyzer.FINISHED_SUCCESS, analyzer.FINISHED_ERROR]:
            self._root.after(self.ANALYZER_CHECK_PERIOD, self._check_analyzer)
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
    def _on_match_spinbox_modified(self, value):
        try:
            match_id = int(value) - 1
        except ValueError:
            return
        mo = self._analyzer.matches[match_id]
        self._update_match_box(mo)
        self._update_tree_view(mo)

    def _update_match_box(self, mo):
        index_start = '1.0+{} chars'.format(mo.start())
        index_end = '1.0+{} chars'.format(mo.end())

        log.debug('Start: {}; End: {};'.format(index_start, index_end))
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

    def _update_tree_view(self, mo):
        self.match_tree.clear()

        anl = self._analyzer
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
            log.debug(item)
            self.match_tree.insert('', tk.END, values=item)


    # def OnBigger(self):
    #     '''Make the font 2 points bigger'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size+2)

    # def OnSmaller(self):
    #     '''Make the font 2 points smaller'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size-2)
