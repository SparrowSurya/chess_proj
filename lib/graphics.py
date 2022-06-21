import math
import colorsys
from PIL import Image, ImageTk, ImageColor

def FlatRectangle(width: int, height: int, color: str, alpha: float):
    """Returns Image of flat color with given alpha."""
    img = Image.new('RGBA', (width, height), color)
    img.putalpha(int(alpha*255))
    return img

def ToImageTk(image: Image):
    """Returns image supported by tkinter from PIL.Image.Image object"""
    return ImageTk.PhotoImage(image)

def CircularGradient(width: int, height: int, color: tuple[str, str], alpha: tuple[float, float]):
    """
    Returns Image with Circular gradient (linear interpolation).

    Params:
        -color: inner_color, outer_color
        -alpha: inner_alpha, outeralpha
    """
    img = Image.new("RGBA", (width, height))
    color = tuple(ImageColor.getcolor(col, "RGB") for col in color)
    max_range = math.sqrt((width//2)**2 + (height//2)**2)
    
    for y in range(height):
        for x in range(width):

            radius = math.sqrt((x - width/2)**2 + (y - height/2)**2)
            radius = float(radius) / max_range

            r = int(color[1][0] * radius + color[0][0] * (1-radius))
            g = int(color[1][1] * radius + color[0][1] * (1-radius))
            b = int(color[1][2] * radius + color[0][2] * (1-radius))
            a = int(((alpha[1] * radius + alpha[0] * (1-radius))**2) * 255)

            img.putpixel((x, y), (r, g, b, a))
    return img


def SatValAlphaGradient(width: int, height: int):
    """Returns alpha Image for HSB color wheel."""
    img = Image.new("RGBA", (width, height), (255,)*4)
    for y in range(height):
        for x in range(width):
            sat = x/width
            val = 1 - y/height
            r, g, b = tuple(round(i * 255) for i in colorsys.hls_to_rgb(0.0, val, 0.0))
            img.putpixel((x, y), (r, g, b, round(255-sat*(val)*255)))
    return img

def HueColorMap(width: int, height: int):
    """Returns Hue color map Image for HSB color wheel."""
    img = Image.new("RGBA", (width, height), (255,)*4)
    for hue in range(width):
        sat = val = 1.0
        r, g, b = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(hue/width,val,sat))
        for i in range(height):
            img.putpixel((hue, i), (r, g, b, 255))
    return img

