import tkinter as tk
import json
from os import path

head, file = path.split(__file__)
FILE = head + "/colors.json"

with open(FILE, 'r') as f:
    colors:dict = json.loads(f.read())

root = tk.Tk()
root.title("Select Color")
# root.resizable(False, False)

main_fr = tk.Frame(root)
main_fr.pack(padx=10, pady=10, fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_fr, width=240)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scroll = tk.Scrollbar(main_fr, orient=tk.VERTICAL, command=canvas.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=1, anchor='e')

canvas.config(yscrollcommand=scroll.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

sec_fr = tk.Frame(canvas, bg='#FFFFFF')
canvas.create_window((0,0), window=sec_fr, anchor=tk.NW)

col_var = tk.StringVar()
col_var.set(colors["Cyan"])


for i, (name, color) in enumerate(colors.items()):
    fr = tk.Frame(sec_fr)
    fr.pack()

    tk.Radiobutton(fr, text=name, value=color, variable=col_var, width=20, justify=tk.LEFT).grid(row=i, column=0, sticky=tk.EW)
    tk.Label(fr, bg=color, width=8).grid(row=i, column=1, sticky=tk.EW)


canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*int(e.delta/120), "units"))
root.mainloop()

