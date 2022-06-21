# file for custom color chooser to replace tkinter colorchooser as to get real time updates

import math
import tkinter as tk
from typing import Callable


class ColorPicker(tk.Frame):
    """
    A class to create custom color picker dialogue box. It will support the realtime color value provider.
    Option to select wheel. 

    Param: -file: (will be removed in future after image being generated using PIL)
        must be an alpha square image of a color wheel.
    
    Param to be added in future:
        -color: to make default pointer pointing to that color .
        -xy: to make default pointer pointing to color a that location if lies in color wheel else will point to default ie #ffffff
    """

    def __init__(self, file: str, master: tk.Frame = None, *args, **kwargs):
        if master is not None: # ERROR
            self.__root = tk.Frame.__init__(master, *args, **kwargs)
            # self.__root = master

        else: # Seperate Window
            self.__root = tk.Tk()
            self.__root.title("ColorPicker")
            self.__root.config(bg='#000000')
        
        self.__file = file # will be replaced in future as soon as rgb wheel gets created

        self.__ptr: list = []
        # POINTER CONFIGURATION
        self.__r: int = 16 # radius

        # COLORWHEEL IMAGE
        self.__img: tk.PhotoImage = tk.PhotoImage(file=self.__file) # modification to be done after __file gets removed
        wd, ht = self.__img.width(), self.__img.height()

        if wd!=ht:
            raise Exception("Image dont have equal dimensions.")
        self.size: int = wd

        # CANVAS
        self.__canvas: tk.Canvas = tk.Canvas(
            self.__root,
            bg="#999999",
            width=  self.size + self.__r*2 + 2,
            height= self.size + self.__r*2 + 2,
            highlightthickness=0
        )
        self.__canvas.pack()

        # COLORWHEEL
        self.ColorWheel = self.__canvas.create_image(self.__r+1, self.__r+1, image=self.__img, anchor=tk.NW)

        # RECENT POINTER
        self.recent = None

        # EVENT BINDING WITH CANVAS
        self.__canvas.bind('<Button-1>', self.Button_12)
        self.__canvas.bind('<B1-Motion>', lambda _e: self.Button_12(_e, bypass_limit=True))


    def new_ptr_coord(self, xy: tuple[int, int] = None) -> tuple[int, int]:
        """Creates the pointer based on x,y coordinates.\n
        Returns the color pointer _id."""
        x, y = self.normalise(xy)
        _id = self.__canvas.create_oval(
            -self.__r + x +1, -self.__r + y +1,
             self.__r + x +1,  self.__r + y +1,
            width=3,
            outline="#EEEEEE",
            fill=self.color(x, y),
            state=tk.NORMAL
        )
        self.__ptr.append(_id)
        self.recent = _id
        return _id
    
    def normalise(self, xy: tuple[int, int], *, edgesnap: bool = False) ->tuple[int, int]:
        """Returns the x, y coordinates."""
        try:
            if xy is None:
                x = y = self.size//2 + self.__r +1
            elif self.onwheel(*xy):
                x, y = xy
            elif edgesnap:
                raise tk.TclError
        except tk.TclError: # lies outside image
            cx = cy = self.__r + self.size//2 + 1
            r = self.size//2
            k = math.dist((cx, cy), xy) - r
            x = int((r*xy[0] + k*cx) / (r+k))
            y = int((r*xy[1] + k*cy) / (r+k))
        finally:
            return x, y
    
    def _move(self, _id, x: int, y: int):
        """Underlying method to move the color pointers ie _id."""
        color = self.color(x, y)
        x0, y0, *_t = self.__canvas.coords(_id)
        dx, dy = x-x0-self.__r, y-y0-self.__r
        self.__canvas.move(_id, dx, dy)
        self.__canvas.itemconfig(_id, fill=color, state=tk.NORMAL)
        self.col = color
        self.recent = _id
    
    def color(self, x: int, y: int):
        """Returns hexadecimal color for x,y."""
        try:
            return "#%02x%02x%02x" % self.__img.get(x-1-self.__r, y-1-self.__r)
        except tk.TclError:
            return None
    
    def onwheel(self, x: int, y: int):
        """Returns True if the x,y is on color wheel."""
        try:
            alpha = self.__img.transparency_get(x-self.__r-1, y-self.__r-1)
            if not alpha: return True

            x0, y0 = self.__canvas.coords(self.ColorWheel)
            x0, y0 = x0+self.size//2, y0+self.size//2

            dist = math.sqrt((x-x0)**2 + (y-y0)**2)
            return False if dist>self.size//2 else True
        except tk.TclError:
            return False
    
    def color_ptr(self, x: int, y: int):
        """Returns relevent color pointer as per parameters."""
        _id = list(self.__canvas.find_closest(x, y))
        _id.remove(self.ColorWheel) if self.ColorWheel in _id else None
        return _id[0] if _id else self.recent
    
    def Button_12(self, _e: tk.Event, *, bypass_limit: bool = False):
        """Function binded to single-left-click and single-left-drag.\n
        bypass_limit: if True then on clicking outside colorwheel it will show movement to the color pointer.
        """
        valid = self.onwheel(_e.x, _e.y)
        _id = self.color_ptr(_e.x, _e.y)
        
        if valid: # Mouse in ColorWheel
            self._move(_id, _e.x, _e.y)
        elif bypass_limit:
            self._move(self.recent, *self.normalise((_e.x, _e.y), edgesnap=True))
        # self.sync_color()
    
    def set_color(self, _id, hex_color: str):
        """Sets location of color pointer ie _id to given color."""
        pass

    def new_ptr_color(self, hex_color: str = None):
        """Makes new pointer based on color.\n
        In case of None sets to default #FFFFFF color.\n
        Returns the color pointer _id."""
        pass
    
    def sync_color(self, func: Callable, *, args: dict, ):
        """Sync to the latest color chosen """
        pass


if __name__ == '__main__':
    widget = ColorPicker("assets/colorwheel.png")
    widget.new_ptr_coord()
    tk.mainloop()


"""NOTE:
Aim to add 2 or wheels of each kind used in daily applications.
PIL might be used in future.

ERROR:
for now providing a different root dont work.
"""