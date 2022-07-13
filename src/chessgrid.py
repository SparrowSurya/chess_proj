import copy

from const import NULL
from lib.utils import *


class ChessGrid():

    def __init__(self):
        self.__grid: list[list[str]] = [[NULL for _ in range(8)] for _ in range(8)]
    
    def __call__(self):
        return copy.deepcopy(self.__grid)
    
    @property
    def grid(self):
        return self.__call__()
    
    @grid.setter
    def grid(self, newgrid: str):
        arr = pid_seq_2_list(newgrid)
        self.__grid = [arr[i*8:(i+1)*8] for i in range(8)]
    
    def __iter__(self):
        for i in range(8):
            for j in range(8):
                yield self.__grid[i][j]

    def __getitem__(self, ids: tuple[int]) -> str:
        if len(ids)==3:
            r, c, p = ids
            return self.__grid[r][c][p]
        elif len(ids)==2:
            r, c = ids
            return self.__grid[r][c]
    
    def __setitem__(self, ids: tuple[int, int], pid: str):
        r, c = ids
        self.__grid[r][c] = pid
    
    def __delitem__(self, ids:tuple[int, int]):
        r, c = ids
        self.__grid[r][c] = NULL
    
    def __str__(self):
        string = '\n'.join([' '.join(row) for row in self.__grid])
        return f"\n{string}"


