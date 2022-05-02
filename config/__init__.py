from config.configure import Default, uConfig
from config.const import MARKING, REF

IPATH = "assets/images/" + uConfig["ipath"]

SQSIZE = int(Default['size'])
CELL_COL1 = Default['col1']
CELL_COL2 = Default['col2']
CELL_SEL0 = Default['sel0']
CELL_SEL1 = Default['sel1']
CELL_SEL2 = Default['sel2']
CHECK = Default['check']
KILL = Default['kill']
BOARD_BORDER = Default['board_border']
MARKING_FONT = Default['marking_font']

P0     : str = REF['player0']
P1     : str = REF['player1']
KING   : str = REF['king']
QUEEN  : str = REF['queen']
KNIGHT : str = REF['knight']
BISHOP : str = REF['bishop']
ROOK   : str = REF['rook']
PAWN   : str = REF['pawn']
NULL   : str = REF['none']
