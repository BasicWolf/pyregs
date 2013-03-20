import time
import tkinter as tk


# From:
# http://code.activestate.com/recipes/464635-call-a-callback-when-a-tkintertext-is-modified/
class ModifiedMixin:
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

        # Set the sentinel.
        self._reseting_modified_flag = True
        self.edit_modified(0)
        self._reseting_modified_flag = False

        # try:
        #     # Set 'modified' to 0.  This will also trigger the <<Modified>>
        #     # virtual event which is why we need the sentinel.
        #     self.tk.call(self._w, 'edit', 'modified', 0)
        # finally:
        #     # Clean the sentinel.
        #     self._reseting_modified_flag = False


myvar = StringVar()
def mywarWritten(*args):
    print "mywarWritten",myvar.get()

myvar.trace("w", mywarWritten)

label = Label(root, textvariable=myvar)
label.pack()

text_entry = Entry(root, textvariable=myvar)
text_entry.pack()

class PRText(ModifiedMixin, tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        ModifiedMixin.__init__(self)

# From:
# http://www.pythonware.com/library/tkinter/introduction/x996-status-bars.htm
class PRStatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    @property
    def text(self):
        return self.label["text"]

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
