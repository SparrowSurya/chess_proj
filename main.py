# -----imports-----
import tkinter as tk

from config import cfg
from src import ChessBoard, ChessGrid, Image, Engine
from const import *


# -----window-----
game = tk.Tk()
game.title("Chess")
game.resizable(False, False)
game.geometry("+600+15")


# -----interface-widgets-----
main: tk.Frame = tk.Frame(
    game,
    bg="#FFFFFF",
    relief=tk.SOLID,
    border=5
)
main.pack()

main_board = tk.Frame(main)
main_board.pack()


# -----loading-backend-----
Config = cfg()
Grid = ChessGrid()
Img = Image()

chessboard = ChessBoard(main_board, Config, Img)
chessboard.canvas.pack()

engine = Engine(chessboard, Grid)


# -----functions-----

# *mouse*
def Mouse_SLC(e: tk.Event):
    """Handles mouse single left click."""
    engine.Clicked('<SLC>', e)

def Mouse_LD(e: tk.Event):
    """bind event for left click drag"""
    engine.Clicked('<LD>', e)

def Mouse_LCR(e: tk.Event):
    """bind event for mouse left click release"""
    engine.Clicked('<LCR>', e)

def Mouse_SRC(e: tk.Event):
    """bind event with single right click"""
    engine.Clicked('<SRC>', e)


# -----menu-----
menubar = tk.Menu(game)
game.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=False)
options_menu = tk.Menu(menubar, tearoff=False)

menubar.add_cascade(label='File', menu=file_menu)
menubar.add_cascade(label='Options', menu=options_menu)

file_menu.add_command(label='New')
file_menu.add_command(label='Open')
file_menu.add_separator()
file_menu.add_command(label='Save')
file_menu.add_separator()
file_menu.add_command(label='Settings')
file_menu.add_separator()
file_menu.add_command(label='Exit', command=game.quit)

options_menu.add_command(label='Play', command=lambda: engine.StartMatch(DEFAULT_GRID))



# -----binding-----
game.bind("<Button-1>", Mouse_SLC)
game.bind("<B1-Motion>", Mouse_LD)
game.bind("<ButtonRelease-1>", Mouse_LCR)
game.bind("<Button-3>", Mouse_SRC)



# -----debug-----
engine.StartMatch()


# -----gameloop-----
game.mainloop()

