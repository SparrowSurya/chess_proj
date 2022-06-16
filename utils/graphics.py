import math
from PIL import Image, ImageTk, ImageColor

def FlatRectangle(width: int, height: int, color: str, alpha: float):
    img = Image.new('RGBA', (width, height), color)
    img.putalpha(int(alpha*255))
    return img

def ToImageTk(image: Image):
    return ImageTk.PhotoImage(image)

# WIP
def CircularGradientRectangle(width: int, height: int, color: tuple[str, str], alpha: tuple[float, float]):
    img = Image.new("RGB", (width, height), (0, 0, 0))
    color = tuple(ImageColor.getcolor(col, "RGB") for col in color)
    max_range = max((width//2)**2, (height//2)**2)
    _r = 0
    _a = 1

    for y in range(height):
        for x in range(width):

            radius = math.sqrt((x - width/2)**2 + (y - height/2)**2)
            radius = float(radius) / max_range

            r = color[0][0] * radius + color[1][0] * (1-radius)
            g = color[0][1] * radius + color[1][1] * (1-radius)
            b = color[0][2] * radius + color[1][2] * (1-radius)
            a = (1-alpha[0])*radius + alpha[1]*radius

            _r, _a = max(radius, _r), min(_a, a)
            img.putpixel((x, y), (int(r), int(g), int(b)))
    print(f"max_radius: {_r} \nmin_alpha: {_a}")
    return img

