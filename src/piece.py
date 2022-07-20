from const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, NULL, P1, MARCH

class Piece:

    def __init__(self, player, row: int, col: int):
        self.player = player
        self.r: int = row
        self.c: int = col

        self.move0: bool = True
        self.alive: bool = True
    
    @property
    def loc(self):
        return self.r, self.c

    def move(self, r: int, c: int):
        self.r, self.c = r, c
        if self.move0:
            self.move0 = False
    
    def march(self, grid: list[list[str]], dr: int, dc: int):
        r, c = self.r+dr, self.c+dc
        way = []
        while (r in range(8) and c in range(8)):
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
    march_dir = MARCH[KING]

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
            else:
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
    march_dir = MARCH[QUEEN]

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
    march_dir = MARCH[KNIGHT]

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
            else:
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
    march_dir = MARCH[ROOK]

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
    march_dir = MARCH[BISHOP]

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
    canmove: bool = True

    def __init__(self, player, row: int, col: int):
        super().__init__(player, row, col)
        self.mdir = -1 if self.player==P1 else 1

    def __call__(self):
        return f"{self.player}{self.alias}"

    def __eq__(self, pid: str):
        return False if not isinstance(pid, str) else self.alias == pid[1]
    
    def move(self, r: int, c: int):
        super().move(r, c)
        if self.r+self.mdir not in range(0, 8):
            self.canmove = False

    def moves(self, grid: list[list[str]]):
        Epos, Apos = [], []
        r = self.r + self.mdir

        if grid[r][self.c] == NULL: # empty 1
            Epos.append((r, self.c))
            
        if (c:=self.c+1) in range(8): # right enemy
            if (pid:=grid[r][c])[0] != self.player and pid != NULL:
                Apos.append((r, c))
                
        if (c:=self.c-1) in range(8): # left enemy
            if (pid:=grid[r][c])[0] != self.player and pid != NULL:
                Apos.append((r, c))
                
        if self.move0 and Epos:
            if r+self.mdir in range(8) and grid[r+self.mdir][self.c] == NULL: # empty 2
                Epos.append((r+self.mdir, self.c))
        return Epos, Apos


'''
class Piece:
    """class to defineall chess piece."""
    def __init__(self, player: str, alias: str, r: int, c: int, **kwargs):
        self.__pl = player
        self.__alias = alias
        self.__r = r
        self.__c = c
        self.__move0 = False
    
        for key, val in kwargs.items():
            self.__setattr__(key, val)

    @property
    def player(self):
        return self.__pl

    @property
    def pid(self):
        return f"{self.__pl}{self.__alias}"

    @property
    def pos(self):
        return self.__r, self.__c
    
    @property
    def move0(self):
        return self.__move0
    
    def __call__(self) -> str:
        return self.pid
    
    def __eq__(self, __o: str) -> bool:
        return self.__alias == __o
    
    @pos.setter
    def pos(self, pos: tuple[int, int]):
        if len(pos)==2:
            _r, _c = pos
            if _r in range(8) and _c in range(8)and isinstance(_r, int) and isinstance(_c, int):
                self.__r, self.__c = _r, _c
                return
        raise Exception(
            "[INVALID PIECE LOCATION]",
            f"argument received: {pos}"
        )

'''
