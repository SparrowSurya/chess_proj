from config import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, NULL, P1

class Piece:
    def __init__(self, player: str, row: int, col: int):
        self.player: str = player
        self.r: int = row
        self.c: int = col

        self.move0: bool = True
        self.alive: bool = True

    def move(self, r: int, c: int):
        self.r, self.c = r, c
    
    def march(self, grid: list[list[str]], dr: int, dc: int):
        r, c = self.r+dr, self.c+dc
        way = []
        while (r in range(8) and c in range(8)): # empty, enemy, friend
            x = grid[r][c]
            if x[0] == NULL: # empty
                way.append((r, c))
            elif x[0] == self.player: # friend
                return way
            else: # enemy
                return way, (r, c)
            r, c = r+dr, c+dc


class King(Piece):
    alias: str = KING
    ischeck: bool = False
    march_dir = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            e, a = self.march(grid, dr, dc)
            Epos.extend(e)
            Apos.extend(a)
        return Epos, Apos


class Queen(Piece):
    alias: str = QUEEN
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            e, a = self.march(grid, dr, dc)
            Epos.extend(e)
            Apos.extend(a)
        return Epos, Apos


class Knight(Piece):
    alias: str = KNIGHT
    march_dir = ((-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            r, c = self.r+dr, self.c+dc
            x = grid[r][c]
            if x[0] == NULL: # empty
                Epos.append((r, c))
            elif x[0] == self.player: # friend
                continue
            else: # enemy
                Apos.append((r, c))
        return Epos, Apos


class Rook(Piece):
    alias: str = ROOK
    march_dir = ((1,0),(0,1),(-1,0),(0,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            e, a = self.march(grid, dr, dc)
            Epos.extend(e)
            Apos.extend(a)
        return Epos, Apos


class Bishop(Piece):
    alias: str = BISHOP
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1))

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            e, a = self.march(grid, dr, dc)
            Epos.extend(e)
            Apos.extend(a)
        return Epos, Apos


class Pawn(Piece):
    alias: str = PAWN
    canmove: bool = False

    def __init__(self, player: str, row: int, col: int):
        super().__init__(player, row, col)
        self.dir = -1 if self.player==P1 else 1

    @property
    def id(self):
        return f"{self.player}{self.alias}"

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        r = self.r + self.dir
        if grid[r][self.c][0] == NULL: # empty 1
            Epos.extend((r, self.c))
        if (c:=self.c+1) in range(8): # right enemy
            if grid[r][c][0]!=self.player:
                Apos.extend((r, c))
        if (c:=self.c-1) in range(8): # left enemy
            if grid[r][c][0] not in (self.player, NULL):
                Apos.extend((r, c))
        if self.move0 and Epos:
            if grid[r+self.dir][self.c][0] == NULL: # empty 2
                Epos.extend((r, self.c))
        return Epos, Apos
