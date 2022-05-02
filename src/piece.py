from config import _Ref

class Piece:
    def __init__(self, player_name: str, row: int, col: int, ipath: str):
        self.player: str = player_name
        self.ipath: str = ipath
        self.r: int = row
        self.c: int = col

        self.move0: bool = True
        self.alive: bool = True

    def moveto(self, r: int, c: int):
        self.r, self.c = r, c
    
    def march(self):
        pass


class King(Piece):
    name: str = "king"
    alias: _Ref = _Ref.king
    ischeck: bool = False
    march_dir = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Queen(Piece):
    name: str = "queen"
    alias: _Ref = _Ref.queen
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Knight(Piece):
    name: str = "knight"
    alias: _Ref = _Ref.knight
    march_dir = ((-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Rook(Piece):
    name: str = "rook"
    alias: _Ref = _Ref.rook
    march_dir = ((1,0),(0,1),(-1,0),(0,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Bishop(Piece):
    name: str = "bishop"
    alias: _Ref = _Ref.bishop
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass


class Pawn(Piece):
    name: str = "pawn"
    alias: _Ref = _Ref.pawn
    canmove: bool = False

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self):
        pass
