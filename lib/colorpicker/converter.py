""""
ColorConversion module.

Provide each color system conversion to RGB and vice-versa.

Format:
    HEX -> str '#XXXXXX'
    RGB -> float [0, 255]
    HSV -> float hue[0, 360) [0, 100]
    HSL -> float hue[0, 360) [0, 100]
    CMYK -> float [0, 100]

"""


def rgb_2_hex(r: float, g: float, b: float) -> str:
    """Returns HEX color code"""
    return '#%02x%02x%02x' % (r, g, b)

def hex_2_rgb(color: str) -> tuple[float, float, float]:
    """Accepts HEX color code"""
    return tuple(color[i+1:i+3] for i in range(0, 3, 2))

def rgb_2_hsv(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Returns HSV.
        h: [0, 360)
        S: [0, 100]
        V: [0, 100]
    """
    r, g, b = r/255, g/255, b/255

    cmax, cmin = max(r, g, b), min(r, g, b)
    diff = cmax-cmin

    if diff==0: h = 0
    elif cmax==r:  h = (60*((g-b)/diff)+360) % 360
    elif cmax==g:  h = (60*((b-r)/diff)+120) % 360
    elif cmax==b:  h = (60*((r-g)/diff)+240) % 360
    
    if cmax: s = (diff/cmax) * 100
    else: s = 0
    
    v = cmax * 100

    return h, s, v

def hsv_2_rgb(h: float, s: float, v: float) -> tuple[float, float, float]:
    """Accepts HSV
        h: [0, 360)
        S: [0, 100]
        V: [0, 100]
    """
    s, v = s/100, v/100
    c = s*v
    x = c*(1-abs((h/60)%2)-1)
    m = v-c

    if (h>=0 and h<60): r, g, b = c, x, 0
    elif (h>=60 and h<120): r, g, b = x, c, 0
    elif (h>=120 and h<180): r, g, b = 0, c, x
    elif (h>=180 and h<240): r, g, b = 0, x, c
    elif (h>=240 and h<300): r, g, b = x, 0, c
    elif (h>=300 and h<360): r, g, b = c, 0, x

    return (r+m)*255, (g+m)*255, (b+m)*255


def rgb_2_hsl(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Returns HSL
        h: [0, 360)
        S: [0, 100]
        L: [0, 100]
    """
    r, g, b = r/255, g/255, b/255

    cmax, cmin = max(r, g, b), min(r, g, b)
    diff = cmax-cmin

    if diff==0: h = 0
    elif cmax==r:  h = (60*((g-b)/diff)+360) % 360
    elif cmax==g:  h = (60*((b-r)/diff)+120) % 360
    elif cmax==b:  h = (60*((r-g)/diff)+240) % 360

    l = ((cmax+cmin)/2) *100

    if diff: s = (diff/(1-abs(2*l -1))) *100
    else: s = 0

    return h, s, l

def hsl_2_rgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    """Accepts HSL
        h: [0, 360)
        S: [0, 100]
        L: [0, 100]
    """
    s, l = s/100, l/100
    c = (1-abs(2*l -1)) *s
    x = c* (1-abs(h/60)%2 -1)
    m = l-c/2

    if (h>=0 and h<60): r, g, b = c, x, 0
    elif (h>=60 and h<120): r, g, b = x, c, 0
    elif (h>=120 and h<180): r, g, b = 0, c, x
    elif (h>=180 and h<240): r, g, b = 0, x, c
    elif (h>=240 and h<300): r, g, b = x, 0, c
    elif (h>=300 and h<360): r, g, b = c, 0, x

    return (r+m)*255, (g+m)*255, (b+m)*255

def cmyk_2_rgb(c: float, m: float, y: float, k: float) -> tuple[float, float, float]:
    """"Accepts CMYK
        c: [0, 100]
        m: [0, 100]
        y: [0, 100]
        k: [0, 100]
    """
    r = 255*(1-c)*(1-k)
    g = 255*(1-m)*(1-k)
    b = 255*(1-y)*(1-k)
    return r, g, b

def rgb_2_cmyk(r: float, g: float, b: float) -> tuple(float, float, float):
    """"Accepts CMYK
        c: [0, 100]
        m: [0, 100]
        y: [0, 100]
        k: [0, 100]
    """
    r, g, b = r/255, g/255, b/255
    k = 1-max(r, g, b)
    c = (1-r-k)/(1-k)
    m = (1-g-k)/(1-k)
    y = (1-b-k)/(1-k)
    return c*100, m*100, y*100, k*100

