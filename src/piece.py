from config.const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, NULL, P1

class Piece:
    def __init__(self, player: str, row: int, col: int):
        self.player: str = player
        self.r: int = row
        self.c: int = col

        self.move0: bool = True
        self.alive: bool = True

    def move(self, r: int, c: int):
        self.r, self.c = r, c
        if self.move0:
            self.move0 = False
    
    def march(self, grid: list[list[str]], dr: int, dc: int):
        r, c = self.r+dr, self.c+dc
        way = []
        while (r in range(8) and c in range(8)): # empty, enemy, friend
            pid = grid[r][c]
            if pid == NULL: # empty
                way.append((r, c))
            elif pid[0] == self.player: # friend
                return way, []
            else: # enemy
                return way, [(r, c)]
            r, c = r+dr, c+dc
        return way, []


class King(Piece):
    alias: str = KING
    ischeck: bool = False
    march_dir = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return self.alias == pid[1]

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            r, c = self.r+dr, self.c+dc
            if r not in range(8) or c not in range(8):
                continue

            pid = grid[r][c]
            if pid == NULL: # empty
                Epos.append((r, c))
            elif pid[0] == self.player: # friend
                continue
            else: # enemy
                Apos.append((r, c))
        return Epos, Apos


class Queen(Piece):
    alias: str = QUEEN
    march_dir = ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return self.alias == pid[1]

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

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return self.alias == pid[1]

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        for dr, dc in self.march_dir:
            r, c = self.r+dr, self.c+dc
            if r not in range(8) or c not in range(8):
                continue

            pid = grid[r][c]
            if pid == NULL: # empty
                Epos.append((r, c))
            elif pid[0] == self.player: # friend
                continue
            else: # enemy
                Apos.append((r, c))
        return Epos, Apos


class Rook(Piece):
    alias: str = ROOK
    march_dir = ((1,0),(0,1),(-1,0),(0,-1))

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return self.alias == pid[1]

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

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return self.alias == pid[1]

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

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return self.alias == pid[1]

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        r = self.r + self.dir
        if grid[r][self.c] == NULL: # empty 1
            Epos.append((r, self.c))
        if (c:=self.c+1) in range(8): # right enemy
            if (pid:=grid[r][c])[0] != self.player and pid != NULL:
                Apos.append((r, c))
        if (c:=self.c-1) in range(8): # left enemy
            if (pid:=grid[r][c])[0] != self.player and pid != NULL:
                Apos.append((r, c))
        if self.move0 and Epos:
            if grid[r+self.dir][self.c] == NULL: # empty 2
                Epos.append((r+self.dir, self.c))
        return Epos, Apos
