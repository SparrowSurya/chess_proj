from config import cfg
from config.const import IDLE, PLAY, PAUSE, P0, P1
from gui.chessboard import ChessBoard
from src.chessgrid import ChessGrid
from src.player import Player

class Match:

    def __init__(self, chessboard: ChessBoard, chessgrid: ChessGrid, config: cfg):
        self.board = chessboard
        self.grid = chessgrid
        self.cfg = config
        
        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)

        self.status: str = IDLE

        self.clicked: list[int, int] = [-1, -1] # x, y
        self.selected: list[tuple[int, int]] = [] # [(rn, cn), ...]

        self.drag: bool = None
        self.check: bool = False

        self.__moves: dict[tuple, tuple] = {} # piece_pos -> (moves, attacks)

