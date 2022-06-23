import tkinter as tk

from lib.colorpicker.base import _ColorPicker
from lib.graphics import SatValAlphaGradient, HueColorMap, ToImageTk


class HSB_colorpicker(_ColorPicker):
    
    def __init__(self, master=None, title='HSV ColorPicker', **kw_attr):
        super().__init__(master, title, **kw_attr)

        self.width = 360
        self.height = (256, 12) # satval, hue 

        self.__satval_img = SatValAlphaGradient(self.width, self.height[0])
        self.__hue_img = HueColorMap(self.width, self.height[1])

        self.__s = 12 # size of color pointer
        self.__h = (5, 12) # size of hue pointer width, height

        self.__widget = tk.Canvas(
            self._root,
            width= self.width + self.__s*2 + 2,
            height= sum(self.height) + self.__s*3 + 2,
            bg='#FFFFFF',
            highlightthickness=0
        )
        self.__widget.pack()

        self.__satval_pimg = ToImageTk(self.__satval_img)
        self.__hue_pimg = ToImageTk(self.__hue_img)

        self._basecol = self.__widget.create_rectangle(
            self.__s+1, self.__s+1,
            self.__s+1+self.width, self.__s+1+self.height[0],
            fill='#FF0000'
        )

        self._ColorRect = self.__widget.create_image(
            self.__s+1, self.__s+1,
            image=self.__satval_pimg,
            anchor=tk.NW
        )

        self._HueRect = self.__widget.create_image(
            self.__s+1, self.__s*2+1+self.height[0],
            image=self.__hue_pimg,
            anchor=tk.NW
        )