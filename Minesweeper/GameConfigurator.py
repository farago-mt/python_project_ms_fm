from tkinter import simpledialog

class GameConfigurator:
    def __init__(self, parent):
        self.parent = parent
        self.rows, self.cols = self.ask_game_area()
        self.mines = self.ask_mine_count()

    def ask_game_area(self):
        default_dimensions = {"row": [10, 5, 15], "column": [10, 5, 20]}
        dimensions = []
        for default_dimension in default_dimensions:
            config = simpledialog.askinteger(
                "Minesweeper",
                f'Please enter {default_dimension} numbers ({default_dimensions[default_dimension][1]}-{default_dimensions[default_dimension][2]}).'
                f'\nCancel to set default ({default_dimensions[default_dimension][0]})',
                minvalue=default_dimensions[default_dimension][1],
                maxvalue=default_dimensions[default_dimension][2]
            )
            print(f'type of {config}: {type(config)}')
            if type(config) == int:
                dimensions.append(config)
            else:
                dimensions.append(default_dimensions[default_dimension][0])
        return dimensions[0], dimensions[1]

    def ask_mine_count(self):
        maxvalue = self.rows * self.cols // 4
        mine_count = simpledialog.askinteger("Minesweeper",
                                             f'How many mines? (1-{maxvalue})\nCancel to set default ({maxvalue})',
                                             minvalue=1,
                                             maxvalue=maxvalue)
        if type(mine_count) == int:
            return mine_count
        else:
            return maxvalue

    #TODO: timer here


