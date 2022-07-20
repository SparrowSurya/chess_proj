from const import PAWN

class Piece:
    """class to define all chess piece."""

    def __init__(self, player: str, piece: str, r: int, c: int, **kwargs):
        self.__player = player
        self.__piece = piece
        self.__r = r
        self.__c = c
        self.__alive = True
        self.__move0 = True
    
        for key, val in kwargs.items():
            self.__setattr__(key, val)
    
    @property
    def r(self):
        return self.__r

    @property
    def c(self):
        return self.__c

    @property
    def player(self):
        return self.__player

    @property
    def piece(self):
        return self.__piece

    @property
    def pid(self):
        return f"{self.__player}{self.__piece}"
    
    @property
    def alive(self):
        return self.__alive

    @property
    def pos(self):
        return self.__r, self.__c
    
    @property
    def move0(self):
        return self.__move0
    
    def goto(self, r: int, c: int):
        if r in range(8) and c in range(8)and isinstance(r, int) and isinstance(c, int):
            self.__r, self.__c = r, c
            self.__move0 = False
            return
        raise Exception(
            "[INVALID PIECE LOCATION]",
            f"argument received: {r, c}"
        )
    
    def __call__(self) -> str:
        return self.pid
    
    def __eq__(self, piece: str) -> bool:
        return self.__piece == piece
    
    def kill(self):
        self.__alive = False

    def promote(self, to_piece: str):
        if self.__piece is PAWN:
            self.__piece = to_piece
        else:
            raise Exception(
                "[INVALID PIECE PROMOTION]",
                f"piece: {self.__piece} "
            )

