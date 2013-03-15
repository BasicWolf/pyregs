from tkinter import Text


# From:
# http://code.activestate.com/recipe/464635-call-a-callback-when-a-tkintertext-is-modified/
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
        self.bind_all('<<Modified>>', self._on_modified)


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


class PRText(ModifiedMixin, Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        ModifiedMixin.__init__(self)

    def on_modified(self, event=None):
        '''
        Override this method do do work when the Text is modified.
        '''
        print('Hi there.')
