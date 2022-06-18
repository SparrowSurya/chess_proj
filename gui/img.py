from tkinter import PhotoImage
from os import path as PATH

from config.const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, P0, P1
from config import ROOT_PATH, REL_IMG_PATH, IMG_DIR

class Image():
    __slots__ = ("__img",)

    __root_path   : str = ROOT_PATH
    __rel_path    : str = REL_IMG_PATH
    __current_path: str = IMG_DIR

    def __init__(self) -> None:
        self.__img = {
            P0: {
                    KING:   PhotoImage(file=f'{self.fullpath}/0K.png'),
                    QUEEN:  PhotoImage(file=f'{self.fullpath}/0Q.png'),
                    KNIGHT: PhotoImage(file=f'{self.fullpath}/0N.png'),
                    BISHOP: PhotoImage(file=f'{self.fullpath}/0B.png'),
                    ROOK:   PhotoImage(file=f'{self.fullpath}/0R.png'),
                    PAWN:   PhotoImage(file=f'{self.fullpath}/0P.png')
                },
            P1: {
                    KING:   PhotoImage(file=f'{self.fullpath}/1K.png'),
                    QUEEN:  PhotoImage(file=f'{self.fullpath}/1Q.png'),
                    KNIGHT: PhotoImage(file=f'{self.fullpath}/1N.png'),
                    BISHOP: PhotoImage(file=f'{self.fullpath}/1B.png'),
                    ROOK:   PhotoImage(file=f'{self.fullpath}/1R.png'),
                    PAWN:   PhotoImage(file=f'{self.fullpath}/1P.png')
                }
            }
    
    @property
    def fullpath(self):
        return f"{self.__root_path}{self.__rel_path}{self.__current_path}"
    
    @property
    def rel_path(self):
        return self.__rel_path
    
    @property
    def current_dir(self):
        return self.__current_path

    def __getitem__(self, pid: str):
        if len(pid)==2:
            pl, pc = pid
            return self.__img[pl][pc]
    
    @current_dir.setter
    def current_path(self, new: str): # to be replaced by dunder method in future after implementing config method
        npath = self.__root_path + self.__rel_path + new

        if PATH.isdir(npath):
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