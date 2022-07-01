MARKING = ("87654321", "abcdefgh")


P0     : str = '0'
P1     : str = '1'
KING   : str = 'k'
QUEEN  : str = 'q'
KNIGHT : str = 'n'
BISHOP : str = 'b'
ROOK   : str = 'r'
PAWN   : str = 'p'
NULL   : str = '..'

NORMAL = 'normal' # to regain its normal color
SELECT = 'select' # to show selection
HIGHLIGHT = 'highlight' # to highlighted ie indirect selection
COLOR_C1 = 'color1' # cell color type 1
COLOR_C2 = 'color2' # cell color type 2
COLOR_CAPTURE = 'unsecure'
COLOR_CHECK = 'check'
COLOR_BORDER = 'border_color'

CELLSIZE = 80
BORDER_WIDTH = 48
FONT_BORDER = ("times new roman", 18, "bold")

IDLE = 'idle'
PLAY = 'playing'
PAUSE = 'paused'

MARCH = {
    KING   : ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)),
    QUEEN  : ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1)),
    KNIGHT : ((-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2)),
    BISHOP : ((1,1),(1,-1),(-1,1),(-1,-1)),
    ROOK   : ((1,0),(0,1),(-1,0),(0,-1))
}

DEFAULT_GRID = "\
0r0n0b0q0k0b0n0r\
0p0p0p0p0p0p0p0p\
................\
................\
................\
................\
1p1p1p1p1p1p1p1p\
1r1n1b1q1k1b1n1r\
"