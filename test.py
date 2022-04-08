import tkinter as tk
from gui.chessboard import ChessBoard


root = tk.Tk()
root.state("zoomed")

c = tk.Canvas(root, bg="green")
c.pack(fill=tk.BOTH, expand=1)

z = ChessBoard(c)

# root.after(3000, lambda: z.select(200, 400))

root.mainloop()