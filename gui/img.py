from tkinter import PhotoImage
from os import path as PATH

from config.const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, P0, P1
from config import ipath, rpath

class Image():
    __slots__ = ("__img",)

    def __init__(self) -> None:
        self.__img = {
            P0: {
                    KING:   PhotoImage(file=f'{ipath}/0K.png'),
                    QUEEN:  PhotoImage(file=f'{ipath}/0Q.png'),
                    KNIGHT: PhotoImage(file=f'{ipath}/0N.png'),
                    BISHOP: PhotoImage(file=f'{ipath}/0B.png'),
                    ROOK:   PhotoImage(file=f'{ipath}/0R.png'),
                    PAWN:   PhotoImage(file=f'{ipath}/0P.png')
                },
            P1: {
                    KING:   PhotoImage(file=f'{ipath}/1K.png'),
                    QUEEN:  PhotoImage(file=f'{ipath}/1Q.png'),
                    KNIGHT: PhotoImage(file=f'{ipath}/1N.png'),
                    BISHOP: PhotoImage(file=f'{ipath}/1B.png'),
                    ROOK:   PhotoImage(file=f'{ipath}/1R.png'),
                    PAWN:   PhotoImage(file=f'{ipath}/1P.png')
                }
            }

    def img(self, player: str, piece: str):
        return self.__img[player][piece]
    
    def update(self, new: str):
        npath = rpath+new

        if PATH.isdir(npath):
            self.__img.clear()
            self.__img = {
                P0: {
                        KING:   PhotoImage(file=f'{npath}/0K.png'),
                        QUEEN:  PhotoImage(file=f'{npath}/0Q.png'),
                        KNIGHT: PhotoImage(file=f'{npath}/0N.png'),
                        BISHOP: PhotoImage(file=f'{npath}/0B.png'),
                        ROOK:   PhotoImage(file=f'{npath}/0R.png'),
                        PAWN:   PhotoImage(file=f'{npath}/0P.png')
                    },
                P1: {
                        KING:   PhotoImage(file=f'{npath}/1K.png'),
                        QUEEN:  PhotoImage(file=f'{npath}/1Q.png'),
                        KNIGHT: PhotoImage(file=f'{npath}/1N.png'),
                        BISHOP: PhotoImage(file=f'{npath}/1B.png'),
                        ROOK:   PhotoImage(file=f'{npath}/1R.png'),
                        PAWN:   PhotoImage(file=f'{npath}/1P.png')
                    }
                }
            return True
        else:
            return False