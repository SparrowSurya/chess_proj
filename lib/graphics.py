import math
from typing import Literal
from PIL import Image, ImageTk, ImageColor

from lib.colorpicker import converter as Convert


def ToImageTk(image: Image):
    """Returns image supported by tkinter from PIL.Image.Image object"""
    return ImageTk.PhotoImage(image)


def FlatRectangle(width: int, height: int, color: str, alpha: float):
    """Returns Image of flat color with given alpha."""
    img = Image.new('RGBA', (width, height), color)
    img.putalpha(int(alpha*255))
    return img


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
            r, g, b = tuple(round(i * 255) for i in Convert.hsl_2_rgb(0.0, 0.0, val))
            img.putpixel((x, y), (r, g, b, round(255-sat*(val)*255)))
    return img


def HueColorMap(width: int, height: int):
    """Returns Hue color map Image for HSB color wheel."""
    img = Image.new("RGBA", (width, height), (255,)*4)
    for hue in range(width):
        sat = val = 1.0
        r, g, b = tuple(round(i * 255) for i in Convert.hsv_2_rgb(hue/width, val, sat))
        for i in range(height):
            img.putpixel((hue, i), (r, g, b, 255))
    return img


def HueSatColorWheel(size: int):
    """Returns the square hue saturation color wheel Image(circular visibility)."""
    img = Image.new("RGBA", (size, size), (255,)*4)
    for y in range(size):
        for x in range(size):
            v1, v2 = (size//2, 0), (x-size//2, y-size//2)
            dist = math.sqrt(((x-size//2)**2 + (y-size//2)**2))

            if dist//1 > size//2:
                img.putpixel((x, y), (0, 0, 0, 0))
                continue

            num = sum(n1*n2 for n1, n2 in zip(v1, v2))
            den = math.sqrt(sum(n*n for n in v1)) * math.sqrt(sum(n*n for n in v2))

            if num==0 and den==0: continue
            
            angle = math.degrees(math.acos(num/den))
            if y>size//2: angle = 360 - angle
            r, g, b = tuple(round(i * 255) for i in Convert.hsv_2_rgb(angle/360, dist/(size//2), 1.0))
            img.putpixel((x, y), (r, g, b, 255))
    return img


def LinearGradient(width: int, height: int, rgba: tuple[int], direction: Literal['x', 'y']): # PENDING
    if direction=='x': dx, dy = 1, 0
    elif direction=='y': dx, dy = 0, 1
    else: raise Exception(
        "[Invalid option] \n",
        f"direction: ({dx, dy})"
    )
    pass
    
    
def CheckerPattern(size: int, color1: str, color2: str):
    """Returns chessboard checker image."""
    color1, color2 = ImageColor.getcolor(color1, "RGB"), ImageColor.getcolor(color2, "RGB")
    img = Image.new("RGB", (size*8, size*8))
    for y in range(size*8):
        for x in range(size*8):
            col = (color1, color2)[(x//size + y//size)%2]
            img.putpixel((x, y), col)
    return img


