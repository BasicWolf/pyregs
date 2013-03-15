import types

import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk
ttk = tkinter.ttk

from .ui_util import PRText
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

        master_frame = ttk.Frame(root)
        master_frame.grid()


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

        txt_pattern = PRText(
            frame,
            height=6,
            width=TEXT_WIDTH_CHARS
        )
        txt_pattern.pack()


        def f(self, event=None):
            print('aa')
#        bind(txt_pattern.on_modified, f)


        #--- setup the analyzed text frame ---#
        #-------------------------------------#
        frame = tk.LabelFrame(
            master_frame,
            text='Processed text',
            bd=2,
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            relief=tk.GROOVE,
            font=self._font
        )
        frame.pack()
        txt_ptext = PRText(
            frame,
            height=10,
            width=TEXT_WIDTH_CHARS
        )
        txt_ptext.pack()

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
        results_frame.pack(fill=tk.X)
        nb = ttk.Notebook(results_frame)
        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()
        nb.pack(fill=tk.BOTH, expand=tk.Y, padx=2, pady=3)

        frame = ttk.Frame(nb)

        msg = ("Ttk is the new Tk themed widget set. One of the widgets "
               "it includes is the notebook widget, which provides a set "
               "of tabs that allow the selection of a group of panels, "
               "each with distinct content. They are a feature of many "
               "modern user interfaces. Not only can the tabs be selected "
               "with the mouse, but they can also be switched between "
               "using Ctrl+Tab when the notebook page heading itself is "
               "selected. Note that the second tab is disabled, and cannot "
               "be selected.")

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

    # def OnBigger(self):
    #     '''Make the font 2 points bigger'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size+2)

    # def OnSmaller(self):
    #     '''Make the font 2 points smaller'''
    #     size = self.customFont['size']
    #     self.customFont.configure(size=size-2)
