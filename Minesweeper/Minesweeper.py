from Cell import Cell
from GameAppearance import GameAppearance
import os
import sys
import tkinter
from tkinter import *
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, parent: object, rows: int, cols: int, number_of_mines: int):
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.number_of_mines = number_of_mines
        self.mine_locations = []
        self.cells = [[None for col in range(cols)] for row in range(rows)]
        self.create_buttons()
        self.place_mines()
        self.calculate_neighbor_mines()

    def create_buttons(self):
        for row in range(self.rows):
            for col in range(self.cols):
                btn = Button(self.parent, width=2, height=2)
                btn.grid(row=row, column=col)
                btn.bind("<Button-1>", self.left_button_pressed)
                btn.bind("<Button-3>", self.flag)
                cell = Cell(btn)
                self.cells[row][col] = cell

    def place_mines(self):
        mine_serials = random.sample(range(self.rows * self.cols), self.number_of_mines)
        for ms in mine_serials:
            row = int(ms / self.cols)
            col = ms % self.cols
            cell = self.cells[row][col]
            self.mine_locations.append([row, col])
            cell.is_mine = True

    def calculate_neighbor_mines(self):
        previous = -1
        next = 1
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                row_values = [row+previous, row, row+next]
                col_values = [col+previous, col, col+next]
                for row_value in row_values:
                    for col_value in col_values:
                        if 0 <= row_value < self.rows and 0 <= col_value < self.cols:
                            cell_checked = self.cells[row_value][col_value]
                            if cell_checked.is_mine:
                                cell.neighbor_mine_counter += 1

    def left_button_pressed(self, event: object):
        widget = event.widget
        grid_info = widget.grid_info()
        row = grid_info.get("row")
        column = grid_info.get("column")
        cell = self.cells[row][column]
        if not cell.is_mine and not cell.is_flagged and cell.neighbor_mine_counter != 0:
            self.reveal(cell)
        if cell.neighbor_mine_counter == 0:
            self.reveal_zero_field(row, column)
        if cell.is_mine and not cell.is_flagged:
            self.show_mines(cell)
            self.game_over()
            return
        self.check_win()

    def reveal(self, cell: Cell):
        cell.button.config(text=str(cell.neighbor_mine_counter),
                           fg=GameAppearance.mine_indicator_colors[cell.neighbor_mine_counter])
        cell.is_revealed = True

    def show_mines(self, cell: Cell):
        for ml in self.mine_locations:
            checked_cell = self.cells[ml[0]][ml[1]]
            checked_cell.button.config(text=GameAppearance.mine_text, fg=GameAppearance.mine_color)

    def reveal_zero_field(self, row: int, col: int):
        if row < 0 or row >= self.rows or col<0 or col >= self.cols or self.cells[row][col].is_revealed:
            return
        if self.cells[row][col].neighbor_mine_counter != 0:
            self.reveal(self.cells[row][col])
            return
        cell = self.cells[row][col]
        self.reveal(cell)
        previous = -1
        next = 1
        row_values = [row+previous, row, row+next]
        col_values = [col+previous, col, col+next]
        for row_value in row_values:
            for col_value in col_values:
                self.reveal_zero_field(row_value, col_value)

    def flag(self, event: object):
        widget = event.widget
        grid_info = widget.grid_info()
        row = grid_info.get("row")
        column = grid_info.get("column")
        cell = self.cells[row][column]
        if not cell.is_flagged and not cell.is_revealed:
            cell.is_flagged = True
            cell.button.config(text=GameAppearance.flag_text)
        elif cell.is_flagged and not cell.is_revealed:
            cell.is_flagged = False
            cell.button.config(text="")

    def game_over(self):
        choice = tkinter.messagebox.askretrycancel("Game Over", "You clicked on a mine!")
        self.restart(choice)

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and cell.neighbor_mine_counter and not cell.is_revealed:
                    return
        choice = tkinter.messagebox.askretrycancel("Congratulation!", "You won!")
        self.restart(choice)

    def restart(self, choice: object):
        if choice:
            os.execl(sys.executable, "main.py", *sys.argv)
        else:
            self.parent.destroy()
