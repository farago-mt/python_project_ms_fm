from tkinter import *
from GameConfigurator import GameConfigurator
from Minesweeper import Minesweeper

def update_title(elapsed_time=0):
    root.title(f'Minesweeper - Time: {elapsed_time} seconds')
    root.after(1000, update_title, elapsed_time + 1)

root = Tk()
root.title("Minesweeper")
# TODO: organize this function to GameConfigurator?
update_title()
root.resizable(False, False)
GameConfigurator = GameConfigurator(root)
print(f'GameConfigurator.rows: {GameConfigurator.rows}, GameConfigurator.cols: {GameConfigurator.cols}, GameConfigurator.mines: {GameConfigurator.mines}')
Minesweeper(root, GameConfigurator.rows, GameConfigurator.cols, GameConfigurator.mines)

root.mainloop()


