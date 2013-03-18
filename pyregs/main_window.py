import types
import re

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk
ttk = tkinter.ttk

from .ui_util import PRText, PRTimer, PRStatusBar
from .util import bind
from .tooltip import ToolTip


class MainWindow:
    def __init__(self, root):
        self._setup_font()
        self._setup_ui(root)

    def _setup_font(self):
        self._font = tkfont.Font(family="Helvetica", size=11)

    def _setup_ui(self, root):
        FRAME_HEIGHT = 120
        FRAME_WIDTH = 240
        TEXT_WIDTH_CHARS = 80

        self._input_timer = PRTimer(root, 300, self._on_input_modified)

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

        self.txt_pattern = PRText(
            frame,
            height=6,
            width=TEXT_WIDTH_CHARS
        )
        self.txt_pattern.pack()
        bind(self.txt_pattern.on_modified, self._input_timer.restart)

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
        self.txt_atext = PRText(
            frame,
            height=10,
            width=TEXT_WIDTH_CHARS
        )
        self.txt_atext.pack()
        bind(self.txt_atext.on_modified, self._input_timer.restart)

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
        self.match_spinbox = tk.Spinbox(results_frame, from_=0, to=10)
        self.match_spinbox.grid(row=0, column=2, sticky=(tk.E,))

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

        msg = 'HELLO WORLD'
        lbl = ttk.Label(frame, wraplength='4i', justify=tk.LEFT, anchor=tk.N,
                        text=msg)
        # position and set resize behaviour
        lbl.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure((0,1), weight=1, uniform=1)
        # add to notebook (underline = index for short-cut character)
        nb.add(frame, text='Description', underline=0, padding=2)

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

        # NEXT FRAME
        frame = ttk.Frame(nb)
        frame.pack(fill='both', expand=True)
        tree_columns = ('Group', 'Value')


        tree = ttk.Treeview(columns=tree_columns, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=vsb.set)
        tree.grid(column=0, row=0, sticky='nsew', in_=frame)
        vsb.grid(column=1, row=0, sticky='ns', in_=frame)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        nb.add(frame, text='Group')

        # STATUS BAR #
        # ---------- #
        self.status_bar = PRStatusBar(master_frame)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_input_modified(self):
        pattern_text = self.txt_pattern.get('0.0', tk.END)
        analyzed_text = self.txt_atext.get('0.0', tk.END)
        pattern_text = pattern_text.strip()
        analyzed_text = analyzed_text.strip()

        if pattern_text == '' or analyzed_text == '':
            return

        self._analyze(pattern_text, analyzed_text)

    def _analyze(self, pattern_text, analyzed_text, flags=0):
        self.status_bar.text = 'Compiling...'
        try:
            reo = re.compile(pattern_text)
            self.status_bar.text = ''
        except Exception:
            self.status_bar.color = 'red'
            self.status_bar.text = 'Error in regular expression pattern'
            return
        mo = reo.match(analyzed_text, flags)
        

    # def OnBigger(self):
    #     '''Make the font 2 points bigger'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size+2)

    # def OnSmaller(self):
    #     '''Make the font 2 points smaller'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size-2)
