"""
For now each color picker will be seperate class as soon as everything gets ready there will be a main colorpicker class
such that we can decide whether to use every color picker in one or seperate or only the selected one appears.

there will also be flexibility to have each type of colorpicker being used seperately


_ColorPicker (base class)
    RGB
    HSB
    HSV
    CMYK
    etc.

        ColorPicker:
            Derived class from _ColorPicker
            which can have multiple colorpicker types or chosen ones
            
"""


# designing base class widget for color picker
import tkinter as tk

class _ColorPicker(tk.Frame):
    """
    Base class for ColorChooser subclasses.
    """

    def __init__(self, master=None, title='ColorPicker', **kw_attr):
        if master is None:
            self.__root = tk.Toplevel()
            self.__root.title(title)
            self.__root.wm_attributes('-resizable', (False, False))
            if kw_attr:
                for key, val in kw_attr: self.__root.wm_attributes(key, val)
        else:
            self.__root = master
    
    @classmethod
    def fromFrame(cls, master, **kwargs):
        """Construct a frame widget with the parent MASTER.

        Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width."""
        tk.Frame.__init__(master=master, **kwargs)
    
    @classmethod
    def fromLabelFrame(cls, master, **kwargs):
        """Construct a labelframe widget with the parent MASTER.

        STANDARD OPTIONS

            borderwidth, cursor, font, foreground, highlightbackground, highlightcolor, highlightthickness, padx, pady, relief, takefocus, text

        WIDGET-SPECIFIC OPTIONS

            background, class, colormap, container, height, labelanchor, labelwidget, visual, width"""
        tk.LabelFrame.__init__(master=master, **kwargs)
    
    @classmethod
    def fromCanvas(cls, master, **kwargs):
        """Construct a canvas widget with the parent MASTER.

        Valid resource names: background, bd, bg, borderwidth, closeenough, confine, cursor, height, highlightbackground, highlightcolor, highlightthickness, insertbackground, insertborderwidth, insertofftime, insertontime, insertwidth, offset, relief, scrollregion, selectbackground, selectborderwidth, selectforeground, state, takefocus, width, xscrollcommand, xscrollincrement, yscrollcommand, yscrollincrement."""
        tk.Canvas.__init__(master=master, **kwargs)

    @property
    def master(self): return self.__root

