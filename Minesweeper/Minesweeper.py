from Cell import Cell
from tkinter import *
import random

class Minesweeper:
    def __init__(self, parent, rows, cols, number_of_mines):
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
        print(mine_serials)
        for ms in mine_serials:
            row = int(ms / self.cols)
            col = ms % self.cols
            # print(f'ms: {ms}, row:{row}, col:{col}')
            cell = self.cells[row][col]
            self.mine_locations.append([row, col])
            cell.is_mine = True
            print(vars(self.cells[row][col]))

    def calculate_neighbor_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # mine_counter = 0
                cell = self.cells[row][col]
                row_values = [row-1, row, row+1]
                col_values = [col-1, col, col+1]
                for row_value in row_values:
                    for col_value in col_values:
                        if 0 <= row_value < self.rows and 0 <= col_value < self.cols:
                            cell_checked = self.cells[row_value][col_value]
                            if cell_checked.is_mine:
                                cell.neighbor_mine_counter += 1
                # print(self.cells[row][col])

    def left_button_pressed(self, event):
        widget = event.widget
        grid_info = widget.grid_info()
        row = grid_info.get("row")
        column = grid_info.get("column")
        cell = self.cells[row][column]
        # print(cell)
        #TODO: reveal cell if they are not mines or flagged - done
        if not cell.is_mine and not cell.is_flagged:
            self.reveal(cell)
        #TODO: reveal zero-field
        #TODO: reveal mine and game over - half-done
        if cell.is_mine:
            self.show_mines(cell)

    def reveal(self, cell: Cell):
        cell.button.config(text=str(cell.neighbor_mine_counter))
        cell.is_revealed = True
        print(f'Mines around: {cell.neighbor_mine_counter}, is_revealed: {cell.is_revealed}')

    #TODO: Show all mines -- DONE
    #TODO: check why background does not change -- low prio
    def show_mines(self, cell: Cell):
        # cell.button.config(text="*", bg="red")
        for ml in self.mine_locations:
            checked_cell = self.cells[ml[0]][ml[1]]
            checked_cell.button.config(text="*")

    #TODO: implement flood fill algorithm
    def reveal_zero_field(self):
        pass

    def flag(self, event):
        widget = event.widget
        grid_info = widget.grid_info()
        row = grid_info.get("row")
        column = grid_info.get("column")
        cell = self.cells[row][column]
        if not cell.is_flagged and not cell.is_revealed:
            cell.is_flagged = True
            cell.button.config(text="X")
            print(f'Flag!! is_flaged: {cell.is_flagged}')
        elif cell.is_flagged and not cell.is_revealed:
            cell.is_flagged = False
            cell.button.config(text="")
            print(f'UNflag!! is_flaged: {cell.is_flagged}')

