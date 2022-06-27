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
from lib.colorpicker.converter import *

class BaseColorPicker(tk.Frame):
    def __init__(self, master=None, callback=None, **kw):
        super().__init__(master, kw)
        self._call = callback

        