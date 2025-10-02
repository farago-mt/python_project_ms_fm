from tkinter import *
from GameConfigurator import GameConfigurator
from Minesweeper import Minesweeper

def update_title(elapsed_time=0):
    root.title(f'Minesweeper - Time: {elapsed_time} seconds')
    root.after(1000, update_title, elapsed_time + 1)

root = Tk()
root.title("Minesweeper")
update_title()
root.resizable(False, False)
GameConfigurator = GameConfigurator(root)
Minesweeper(root, GameConfigurator.rows, GameConfigurator.cols, GameConfigurator.mines)
root.mainloop()


