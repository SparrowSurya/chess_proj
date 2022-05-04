MARKING = ("12345678", "abcdefgh")

REF = {
    'player0': '0',
    'player1': '1',
    'king'   : 'k',
    'queen'  : 'q',
    'knight' : 'n',
    'bishop' : 'b',
    'rook'   : 'r',
    'pawn'   : 'p',
    'none'   : '.'
}


P0     : str = REF['player0']
P1     : str = REF['player1']
KING   : str = REF['king']
QUEEN  : str = REF['queen']
KNIGHT : str = REF['knight']
BISHOP : str = REF['bishop']
ROOK   : str = REF['rook']
PAWN   : str = REF['pawn']
NULL   : str = REF['none']


DEFAULT_GRID = "\
0r0n0b0k0q0b0n0r\
0p0p0p0p0p0p0p0p\
................\
................\
................\
................\
1p1p1p1p1p1p1p1p\
1r1n1b1k1q1b1n1r\
"