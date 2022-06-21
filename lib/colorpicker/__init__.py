"""
# --------------------------------------------------------------------------------
HSB:

from PIL import Image, ImageTk
import colorsys
from os import path


wd, ht = 360, 256
im = Image.new("RGBA", (wd, ht), (255,)*4)

for y in range(ht):
    for x in range(wd):
        sat = (x/wd)
        val = (1 - (y/ht))
        r, g, b = tuple(round(i * 255) for i in colorsys.hls_to_rgb(0.0, val, 0.0))
        im.putpixel((x, y), (r, g, b, round(255-sat*(val)*255)))


ht_hue = 30
im_hue = Image.new("RGBA", (wd, ht_hue), (255,)*4)

for hue in range(wd):
    sat = val = 1.0
    r, g, b = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hue/wd,val,sat))
    for i in range(ht_hue):
        im_hue.putpixel((hue, i), (r, g, b, 255))


from tkinter import *

root = Tk()

canvas = Canvas(root, bg='white', width=wd, height=ht+ht_hue+2, highlightthickness=0)
canvas.pack(padx=10, pady=10)

flat = canvas.create_rectangle(0, 0, wd, ht, fill="#FF0000", width=0)

img = ImageTk.PhotoImage(im)
item = canvas.create_image(0, 0, image=img, anchor=NW)

img_hue = ImageTk.PhotoImage(im_hue)
item_hue = canvas.create_image(0, ht+2, image=img_hue, anchor=NW)


def update(e):
    global canvas, flat
    hue = round(float(e))
    canvas.itemconfig(flat, fill="#%02x%02x%02x" % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hue/wd,1,1)))


slider = Scale(root, from_=0, to=360, length=wd, orient=HORIZONTAL, command=update)
slider.pack(padx=10, pady=5)

root.mainloop()


# --------------------------------------------------------------------------------

RGB:


# --------------------------------------------------------------------------------
"""