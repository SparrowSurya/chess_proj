import math
import tkinter as tk
from typing import Callable

from lib.graphics import ToImageTk, HueSatColorWheel
from .base import _ColorPicker

class ColorPicker(_ColorPicker):
    """
    A class to create custom color picker dialogue box. It will support the realtime color value provider.
    Option to select wheel. 
    
    Param to be added in future:
        -color: to make default pointer pointing to that color .
        -xy: to make default color pointer pointing to color at that location if lies in color wheel else will point to default ie #ffffff
    """

    def __init__(self, master= None, title="RGB", *args, **kwargs):
        super().__init__(master, title)
        
        self.__ptr: list = []
        self.__r: int = 16 # radius of color pointer
        self.size = 210 # dimensions of image

        # CANVAS
        self.__widget: tk.Canvas = tk.Canvas(
            self._root,
            bg="#999999",
            width=  self.size + self.__r*2 + 2,
            height= self.size + self.__r*2 + 2,
            highlightthickness=0
        )
        self.__widget.pack()

        # COLORWHEEL IMAGE
        self.__im = HueSatColorWheel(self.size)
        self.__img = ToImageTk(self.__im)

        # COLORWHEEL
        self.ColorWheel = self.__widget.create_image(self.__r+1, self.__r+1, image=self.__img, anchor=tk.NW)

        # RECENT POINTER
        self.recent = None

        # EVENT BINDING WITH CANVAS
        self.__widget.bind('<Button-1>', self.Button_12)
        self.__widget.bind('<B1-Motion>', lambda _e: self.Button_12(_e, bypass_limit=True))

        if isinstance(self._root, tk.Tk): self._root.mainloop()

    
    def pix(self, x: int, y: int):
        """Returns the pixel color at given coordinate. coordinates must lie on Image else returns None."""
        try:
            col = self.__im.getpixel((x, y))
            # if col[3]!=255: col = None
        except IndexError: col = None
        finally: return col

    def onwheel(self, x: int, y: int):
        """Returns True if the x,y is on color wheel. x,y is wrt to colorwheel widget."""
        try:
            x0, y0 = tuple(map(int, self.__widget.coords(self.ColorWheel)))
            if (x not in range(x0, x0+self.size) or
                y not in range(y0, y0+self.size)): return False

            if self.pix(x-x0, y-y0)[3]!=255: return False

            x0, y0 = x0+self.size//2, y0+self.size//2
            dist = math.sqrt((x-x0-1)**2 + (y-y0-1)**2)
            return False if dist>self.size//2 else True
            
        except (tk.TclError or IndexError):
            return False

    def normalise(self, xy: tuple[int, int], *, edgesnap: bool = False) ->tuple[int, int]:
        """Returns the normalised x, y coordinates. x,y is wrt to colorwheel widget.

        Param:
            -edgesnap: if True returns the closest pixel wrt to center of colorwheel.
        """
        try:
            if xy is None: # x, y = center of colorwheel
                x = y = self.size//2 + self.__r +1
            elif self.onwheel(*xy): # x, y
                x, y = xy
            elif edgesnap:
                raise tk.TclError
        except tk.TclError: # lies outside image
            c = self.__r + self.size//2 + 1
            r = self.size//2
            e = math.dist((c, c), xy) - r
            x = (r*xy[0] + e*c) / (r+e)
            y = (r*xy[1] + e*c) / (r+e)
        finally:
            return round(x), round(y)

    def new_ptr_by_coord(self, xy: tuple[int, int] = None) -> tuple[int, int]:
        """Creates the pointer based on x,y coordinates. x,y is wrt to colorwheel widget.\n
        Returns the color pointer _id."""
        x, y = self.normalise(xy)
        _id = self.__widget.create_oval(
            -self.__r + x+1, -self.__r + y+1,
             self.__r + x+1,  self.__r + y+1,
            width=3,
            outline="#FFFFFF",
            fill=self.color(x, y),
            state=tk.NORMAL
        )
        self.__ptr.append(_id)
        self.recent = _id
        return _id

    def new_ptr_by_color(self, hex_color: str = None):
        """Makes new pointer based on color.\n
        In case of None sets to default #FFFFFF color.\n
        Returns the color pointer _id."""
        pass

    def _move(self, _id, x: int, y: int):
        """Underlying method to move the color pointers ie _id."""
        # if (color:=self.color(x, y))==None: return
        color = self.color(x, y)
        x0, y0, *_t = self.__widget.coords(_id)
        dx, dy = x-x0-self.__r, y-y0-self.__r
        self.__widget.move(_id, dx, dy)
        self.__widget.itemconfig(_id, fill=color, state=tk.NORMAL)
        self.col = color
        self.recent = _id
        self.call()
    
    def color(self, x: int, y: int):
        """Returns hexadecimal color for x,y. x,y is wrt to colorwheel widget."""
        try:  col = self.pix(x-1-self.__r, y-1-self.__r)
        except (tk.TclError or IndexError or TypeError): col = None
        finally:
            if col is None: return col
            else: return "#%02x%02x%02x" % col[:3]

    def ptr(self, x: int, y: int):
        """Returns relevent color pointer as per parameters."""
        _id = list(self.__widget.find_closest(x, y))
        _id.remove(self.ColorWheel) if self.ColorWheel in _id else None
        return _id[0] if _id else self.recent
    
    def Button_12(self, _e: tk.Event, *, bypass_limit: bool = False):
        """Function binded to single-left-click and single-left-drag.\n
        bypass_limit: if True then on clicking outside colorwheel it will show movement to the color pointer.
        """
        if not self.__ptr: return

        valid = self.onwheel(_e.x, _e.y)
        _id = self.ptr(_e.x, _e.y)
        
        if valid: # Mouse in ColorWheel
            self._move(_id, _e.x, _e.y)
        elif bypass_limit:
            self._move(self.recent, *self.normalise((_e.x, _e.y), edgesnap=True))
    
    def set_color(self, _id, hex_color: str):
        """Sets location of color pointer ie _id to given color."""
        pass

    def call(self):
        """Returns the realtime selected color 'HEX'."""
        return self._call(self.__widget.itemcget(self.recent, 'fill'))


"""NOTE:
Aim to add 2 or wheels of each kind used in daily applications.
PIL might be used in future.

ERROR:
some errors on pixel calculation 
    -widget starting coords arent 0 0
"""

