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
    alias: str = 'K'
    ischeck: bool = False
    march_dir = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

    def moves(self):
        pass


class Queen(Piece):
    name: str = "queen"
    alias: str = 'Q'
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))

    def moves(self):
        pass


class Knight(Piece):
    name: str = "knight"
    alias: str = 'N'
    march_dir = ((-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2))

    def moves(self):
        pass


class Rook(Piece):
    name: str = "rook"
    alias: str = 'R'
    march_dir = ((1,0),(0,1),(-1,0),(0,-1))

    def moves(self):
        pass


class Bishop(Piece):
    name: str = "bishop"
    alias: str = 'B'
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1))

    def moves(self):
        pass


class Pawn(Piece):
    name: str = "pawn"
    alias: str = 'P'
    canmove: bool = False

    def moves(self):
        pass
