import time
import tkinter as tk
import tkinter.ttk as ttk
from idlelib.WidgetRedirector import WidgetRedirector


# From:
# http://code.activestate.com/recipes/464635-call-a-callback-when-a-tkintertext-is-modified/
class TextModifiedMixin:
    """Class to allow a Tkinter Text widget to notice when it's modified.

    To use this mixin, subclass from Tkinter.Text and the mixin, then write
    an __init__() method for the new class that calls _init().
    Then override the on_modified() method to implement the behavior that
    you want to happen when the Text is modified.
    """
    def __init__(self):
        """Prepare the Text for modification notification."""
        # Clear the modified flag, as a side effect this also gives the
        # instance a _reseting_modified_flag attribute.
        self._clear_modified_flag()

        # Bind the <<Modified>> virtual event to the internal callback.
        self.bind('<<Modified>>', self._on_modified)


    def _on_modified(self, event=None):
        """ Call the user callback. Clear the Tk 'modified' variable
        of the Text."""
        # If this is being called recursively as a result of the call to
        # _clear_modified_flag() immediately below, then we do nothing.
        if self._reseting_modified_flag:
            return

        # Clear the Tk 'modified' variable.
        self._clear_modified_flag()

        # Call the user-defined callback.
        self.on_modified(event)

    def on_modified(self, event=None):
        """Override this method in your class to do what you want when
        the Text is modified."""
        pass

    def _clear_modified_flag(self):
        """Clear the Tk 'modified' variable of the Text.

        Uses the _reseting_modified_flag attribute as a sentinel against
        triggering _on_modified() recursively when setting 'modified' to 0.
        """
        self._reseting_modified_flag = True
        self.edit_modified(0)
        self._reseting_modified_flag = False


class EntryModifiedMixin:
    def __init__(self):
        self._var = tk.StringVar()
        self._var.trace('w', self._on_modified)
        self.config(textvariable=self._var)

    def _on_modified(self, *args):
        self.on_modified(self._var.get())

    def on_modified(self, value):
        pass


class PRText(TextModifiedMixin, tk.Text):
    def __init__(self, master, *args, **kwargs):
        scrollbar = ttk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        kwargs.update(dict(wrap=tk.WORD, yscrollcommand=scrollbar.set))
        tk.Text.__init__(self, master, *args, **kwargs)
        scrollbar.config(command=self.yview)
        self._setup_menu(master)
        TextModifiedMixin.__init__(self)

    def _setup_menu(self, master, editable=True):
        #--- Textboxes popoup menu ---#
        menu = tk.Menu(tearoff=0)
        cmd_cut = lambda: self.event_generate("<<Cut>>")
        cmd_copy = lambda: self.event_generate("<<Copy>>")
        cmd_paste = lambda: self.event_generate("<<Paste>>")

        if editable:
            menu.add_command(label="Cut", command=cmd_cut)

        menu.add_command(label="Copy", command=cmd_copy)

        if editable:
            menu.add_command(label="Paste", command=cmd_paste)

        def popup_menu(event):
            menu.post(event.x_root, event.y_root)
            menu.focus_set()

        def popupFocusOut(self,event=None):
            menu.unpost()

        self.bind('<Button-3>', popup_menu)
        menu.bind("<FocusOut>",popupFocusOut)

    def clear(self):
        self.delete(1.0, tk.END)

    @property
    def text(self):
        return self.get(0.0, tk.END)

    @text.setter
    def text(self, value):
        self.clear()
        self.insert(0.0, value)



class PRReadonlyText(PRText):
    def __init__(self, *args, **kwargs):
        PRText.__init__(self, *args, **kwargs)
        self._insert = self.insert
        self._delete = self.delete
        self._redirector = WidgetRedirector(self)
        self.readonly = True

    def _setup_menu(self, master, editable=False):
        super(PRReadonlyText, self)._setup_menu(master, editable=False)
        
    def clear(self):
        self.readonly = False
        self._delete(1.0, tk.END)
        self.readonly = True

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        _break_func = lambda *args, **kw: 'break'
        if value:
            self.insert = self._redirector.register('insert', _break_func)
            self.delete = self._redirector.register('delete', _break_func)
        else:
            self.insert = self._redirector.unregister('insert')
            self.delete = self._redirector.unregister('delete')
        self._readonly = value

    @property
    def text(self):
        return self.get(0.0, tk.END)

    @text.setter
    def text(self, value):
        self.readonly = False
        self._delete(0.0, tk.END)
        self._insert(0.0, value)
        self.readonly = True


class PRTreeview(ttk.Treeview):
    def clear(self):
        tree_elems = self.get_children()
        for elem in tree_elems:
            self.delete(elem)


class PRSpinbox(EntryModifiedMixin, tk.Spinbox):
    def __init__(self, *args, **kwargs):
        tk.Spinbox.__init__(self, *args, **kwargs)
        EntryModifiedMixin.__init__(self)

    def clear(self):
        self.delete(0, tk.END)

    @property
    def text(self):
        return self.get(0, tk.END)

    @text.setter
    def text(self, value):
        self.clear()
        self.insert(0, value)

# From:
# http://www.pythonware.com/library/tkinter/introduction/x996-status-bars.htm
class PRStatusBar(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W, **kwargs)
        self.label.pack(fill=tk.X)

    @property
    def text(self):
        return self.label['text']

    @text.setter
    def text(self, text):
        self.label.config(text=text)
        self.label.update_idletasks()

    @property
    def color(self):
        return self.label['fg']

    @color.setter
    def color(self, color_string):
        self.label.config(fg=color_string)
        self.label.update_idletasks()


class PRCheckbutton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        self._var = tk.IntVar()
        self._var.trace('w', self._on_modified)
        kwargs.update(dict(variable=self._var))
        tk.Checkbutton.__init__(self, *args, **kwargs)

    def _on_modified(self, *args):
        self.on_modified(self._var.get() == 1)

    def on_modified(self, checked):
        pass

    @property
    def checked(self):
        return self._var.get() == 1

    @checked.setter
    def checked(self, value):
        val = int(value == True)
        self._var.set(val)


class Timer:
    BASE_TICK = 100

    def __init__(self, tk, period, callback):
        self._tk = tk
        self.started = False
        self.callback = callback
        self.started_time = 0
        self.period = period / 1000
        self._tick()

    def restart(self, *args, **kwargs):
        self.started = True
        self.started_time = time.time()

    def stop(self):
        self.started = False

    def _tick(self):
        if self.started and time.time() - self.started_time > self.period:
            self.started = False
            self.callback()
        self._tk.after(self.BASE_TICK, self._tick)

