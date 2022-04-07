import tkinter as tk
from gui.chessboard import ChessBoard


root = tk.Tk()

c = tk.Canvas(root, bg="green")
c.pack(fill=tk.BOTH, expand=1)

z = ChessBoard(c)
z.draw()

# root.after(3000, lambda: z.select(200, 400))

root.mainloop()