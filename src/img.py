from tkinter import PhotoImage
from os import path as PATH

from const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, P0, P1
from config import ROOT_PATH, IMG_DIR
from lib.utils import check_pid


class Image():
    __root_path   : str = ROOT_PATH
    __rel_path    : str = "\\assets\\images\\"
    __current_path: str = IMG_DIR

    def __init__(self) -> None:
        self.__img = {
            P0: {
                    KING:   PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\0K.png'),
                    QUEEN:  PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\0Q.png'),
                    KNIGHT: PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\0N.png'),
                    BISHOP: PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\0B.png'),
                    ROOK:   PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\0R.png'),
                    PAWN:   PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\0P.png')
                },
            P1: {
                    KING:   PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\1K.png'),
                    QUEEN:  PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\1Q.png'),
                    KNIGHT: PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\1N.png'),
                    BISHOP: PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\1B.png'),
                    ROOK:   PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\1R.png'),
                    PAWN:   PhotoImage(file=f'{self.__root_path}{self.__rel_path}\\1P.png')
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
        check_pid(pid)
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
            self.__current_path = new
            return True
        else:
            return False