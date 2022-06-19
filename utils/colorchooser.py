# file for custom color chooser to replace tkinter colorchooser as to get real time updates

import math
from tkinter import *

class ColorChooser:
    """
    A class to create custom color picker dialogue box.

    Param: -file:
        must be an alpha square image of a color wheel.
    """
    def __init__(self, file: str):
        self.__file = file
        self.__ptr: list = []

        # WINDOW
        self.__root = Tk()
        self.__root.title("ColorChooser")
        self.__root.config(bg='#000000')

        # POINTER CONFIGURATION
        self.__r: int = 16 # radius

        # COLORWHEEL IMAGE
        self._img: PhotoImage = PhotoImage(file=self.__file)
        wd, ht = self._img.width(), self._img.height()

        if wd!=ht:
            raise Exception("Image dont have equal dimensions.")
        self.size: int = wd

        # CANVAS
        self.canvas: Canvas = Canvas(
            self.__root,
            bg="#999999",
            width=  self.size + self.__r*2 + 2,
            height= self.size + self.__r*2 + 2,
            highlightthickness=0
        )
        self.canvas.pack()

        # COLORWHEEL
        self.ColorWheel = self.canvas.create_image(self.__r+1, self.__r+1, image=self._img, anchor=NW)

        # RECENT POINTER
        self.recent = None

        # EVENT BINDING WITH CANVAS
        self.canvas.bind('<Button-1>', self.Button_12)
        self.canvas.bind('<B1-Motion>', lambda _e: self.Button_12(_e, bypass_range=True))


    def newptr(self, xy: tuple[int, int] = None) -> tuple[int, int]:
        """Returns the final x,y coordinates."""
        x, y = self._flatten(xy)
        ptr = self.canvas.create_oval(
            -self.__r + x +1, -self.__r + y +1,
             self.__r + x +1,  self.__r + y +1,
            width=3,
            outline="#EEEEEE",
            fill=self._get_hex(x, y),
            state=NORMAL
        )
        self.__ptr.append(ptr)
        self.recent = ptr
        return x, y
    
    def _flatten(self, xy: tuple[int, int]) ->tuple[int, int]:
        """Corrects the x, y coordinates when not in proper place"""
        try:
            if xy is None or self._img.transparency_get(*xy): # IsAlpha
                x = y = self.size//2 + self.__r +1
        except TclError: # lies outside image
            cx = cy = self.__r + self.size//2 + 1
            r = self.size//2
            k = math.dist((cx, cy), xy) - r
            x = int((r*xy[0] + k*cx) / (r+k))
            y = int((r*xy[1] + k*cy) / (r+k))
        finally:
            return x, y
    
    def _move(self, _id, x: int, y: int):
        """Underlying method to move the color pointers."""
        color = self._get_hex(x, y)
        x0, y0, *_t = self.canvas.coords(_id)
        dx, dy = x-x0-self.__r, y-y0-self.__r
        self.canvas.move(_id, dx, dy)
        self.canvas.itemconfig(_id, fill=color, state=NORMAL)
        self.col = color
        self.recent = _id
    
    def _get_hex(self, x: int, y: int):
        """Returns hexadecimal color for x,y."""
        try:
            return "#%02x%02x%02x" % self._img.get(x-1-self.__r, y-1-self.__r)
        except TclError:
            return None
    
    def onwheel(self, x: int, y: int):
        """
        Return  True if the x,y is on color wheel.
        """
        try:
            alpha = self._img.transparency_get(x-self.__r-1, y-self.__r-1)
            if not alpha: return True

            x0, y0 = self.canvas.coords(self.ColorWheel)
            x0, y0 = x0+self.size//2, y0+self.size//2

            dist = math.sqrt((x-x0)**2 + (y-y0)**2)
            return False if dist>self.size//2 else True
        except TclError:
            return False
    
    def _get_ptr(self, x: int, y: int):
        """Returns relevent color pointer as per parameters."""
        _id = list(self.canvas.find_closest(x, y))
        _id.remove(self.ColorWheel) if self.ColorWheel in _id else None
        return _id[0] if _id else self.recent
    
    def Button_12(self, _e: Event, *, bypass_range: bool = False):
        """
        Function binded to single-left-click and single-left-drag.

        bypass_range: if True then on clicking outside colorwheel it will show movement to the color pointer.
        """
        valid = self.onwheel(_e.x, _e.y)
        _id = self._get_ptr(_e.x, _e.y)
        
        if valid: # Mouse in ColorWheel
            self._move(_id, _e.x, _e.y)
        else:
            if bypass_range:
                self._move(self.recent, *self._flatten((_e.x, _e.y)))
    
    


if __name__ == '__main__':
    cc = ColorChooser("assets/colorwheel.png")
    cc.newptr()
    mainloop()
