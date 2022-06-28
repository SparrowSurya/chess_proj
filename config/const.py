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

NORMAL = 'normal'
SELECT = 'select'
HIGHLIGHT = 'highlight'
COLOR_C1 = 'color1' # cell color type 1
COLOR_C2 = 'color2' # cell color type 2
COLOR_KILL = 'kill'
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
0r 0n 0b 0k 0q 0b 0n 0r\n\
0p 0p 0p 0p 0p 0p 0p 0p\n\
.. .. .. .. .. .. .. ..\n\
.. .. .. .. .. .. .. ..\n\
.. .. .. .. .. .. .. ..\n\
.. .. .. .. .. .. .. ..\n\
1p 1p 1p 1p 1p 1p 1p 1p\n\
1r 1n 1b 1k 1q 1b 1n 1r\
"