from src import Game

def main():
    game = Game()
    game.gui.mainloop()


if __name__ == "__main__":
    main()

"""
-----imports-----
import tkinter as tk

-----window-----
win = tk.Tk()
win.title("Chess")
win.resizable(False, False)

# basic container
-----interface-widgets-----
win._main: tk.Frame = tk.Frame(
    win,
    bg="#FFFFFF",
    relief=tk.SOLID,
    border=5
)
win._main.pack()

# chessboard lies in this widget
win._main_board = tk.Frame(win._main)
win._main_board.pack()

win.chessboard: ChessBoard = ChessBoard(win._main_board, CONFIG)
win.chessboard.canvas.pack()


-----loading-backend-----
CONFIG: cfg = cfg()

-----menu-----
win.menubar = tk.Menu(win)
win.config(menu=win.menubar)

    def NewMenu(win, name: str):
        menu = tk.Menu(win.menubar, tearoff=False)
        win.menubar.add_cascade(label=name, menu=menu)
        return menu

-----binding-----

win.mainloop()
"""