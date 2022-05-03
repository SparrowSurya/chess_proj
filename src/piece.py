from config import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN

class Piece:
    def __init__(self, player: str, row: int, col: int):
        self.player: str = player
        self.r: int = row
        self.c: int = col

        self.move0: bool = True
        self.alive: bool = True

    def move(self, r: int, c: int):
        self.r, self.c = r, c
    
    def march(self):
        pass


class King(Piece):
    name: str = "king"
    alias: str = KING
    ischeck: bool = False
    march_dir = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Queen(Piece):
    name: str = "queen"
    alias: str = QUEEN
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Knight(Piece):
    name: str = "knight"
    alias: str = KNIGHT
    march_dir = ((-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Rook(Piece):
    name: str = "rook"
    alias: str = ROOK
    march_dir = ((1,0),(0,1),(-1,0),(0,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Bishop(Piece):
    name: str = "bishop"
    alias: str = BISHOP
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Pawn(Piece):
    name: str = "pawn"
    alias: str = PAWN
    canmove: bool = False

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass
