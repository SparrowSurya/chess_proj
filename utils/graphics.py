import math
from PIL import Image, ImageTk, ImageColor

def FlatRectangle(width: int, height: int, color: str, alpha: float):
    img = Image.new('RGBA', (width, height), color)
    img.putalpha(int(alpha*255))
    return img

def ToImageTk(image: Image):
    return ImageTk.PhotoImage(image)

def CircularGradient(width: int, height: int, color: tuple[str, str], alpha: tuple[float, float]):
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

