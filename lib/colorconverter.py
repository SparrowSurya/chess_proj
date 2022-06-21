# MAIN: RGB HSV
# OPTIONAL: HSL HWB CMYK

import colorsys

def rgb_2_hex(r: int, g: int, b: int) -> str:
    return '#%02x%02x%02x' % (r, g, b)

def hex_2_rgb(color: str) -> tuple[int, int, int]:
    return tuple(color[i+1:i+3] for i in range(0, 3, 2))

def rgb_2_hsv(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Returns HSV.
        H: [0, 360)
        S: [0, 100]
        V: [0, 100]
    """
    r, g, b = r/255, g/255, b/255

    cmax, cmin = max(r, g, b), min(r, g, b)
    diff = cmax-cmin

    # hue 
    if cmax==cmin: h = 0
    elif cmax==r:  h = (60*((g-b)/diff)+360) % 360
    elif cmax==g:  h = (60*((b-r)/diff)+120) % 360
    elif cmax==b:  h = (60*((r-g)/diff)+240) % 360
    
    # saturation 
    if cmax: s = (diff/cmax) * 100
    else: s = 0
    
    # value 
    v = cmax * 100

    return h, s, v

def hsv_2_rgb(h: int, s: int, v: int) -> tuple[int, int, int]:
    """Returns RGB
        H: [0, 360)
        S: [0, 100]
        V: [0, 100]
    """
    pass

def rgb_2_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Returns HSL
        H: [0, 360)
        S: [0, 100]
        L: [0, 100]
    """
    pass

def hsl_2_rgb(h: int, s: int, v: int) -> tuple[int, int, int]:
    """Returns RGB
        H: [0, 360)
        S: [0, 100]
        L: [0, 100]
    """
    


def cmyk_2_rgb():
    pass

def rgb_2_cmyk():
    pass