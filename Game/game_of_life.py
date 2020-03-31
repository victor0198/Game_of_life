import json
import time
import numpy
import sys
from tkinter import *


class Grid(object):
    def __init__(self, grid, objs=None, style=None):
        self.generation = 0
        self.grid = grid

        if objs is not None:
            self.graphics = True
            self.root = objs[0]
            self.canvas = objs[1]
            self.label = objs[2]
            if style is not None:
                self.cell_size = style[0]
                self.line_width = style[1]
            else:
                self.cell_size = 18
                self.line_width = 2
        else:
            self.graphics = False

        self.last_keypress = time.time()

    # make a 2D array with the number of neighbours
    def neighbours(self):
        neighbours_map = []
        rows = self.grid.shape[0]
        cols = self.grid.shape[1]
        for row_idx in range(rows):
            this_row = []
            for col_idx in range(cols):
                neighbours_coord = [
                    ((row_idx - 1 + rows) % rows, (col_idx - 1) % cols),
                    (row_idx % rows, (col_idx - 1 + cols) % cols),
                    ((row_idx + 1) % rows, (col_idx - 1 + cols) % cols),
                    ((row_idx + 1) % rows, col_idx),
                    ((row_idx + 1) % rows, (col_idx + 1) % cols),
                    (row_idx % rows, (col_idx + 1 + cols) % cols),
                    ((row_idx - 1 + rows) % rows, (col_idx + 1) % cols),
                    ((row_idx - 1 + rows) % rows, col_idx)
                ]
                this_row.append(sum(self.grid[n_x][n_y] for n_x, n_y in neighbours_coord))
            neighbours_map.append(this_row)
        return neighbours_map

    # make changes in the grid according to number of neighbours
    def next_generation(self, n_map):
        for row_idx in range(self.grid.shape[0]):
            for col_idx in range(self.grid.shape[1]):
                i = (self.cell_size + self.line_width) * col_idx
                j = (self.cell_size + self.line_width) * row_idx
                if (n_map[row_idx][col_idx] == 3 and self.grid[row_idx][col_idx] == 0) or \
                        ((n_map[row_idx][col_idx] == 3 or n_map[row_idx][col_idx] == 2) and self.grid[row_idx][
                            col_idx] == 1):
                    if self.grid[row_idx][col_idx] == 0:
                        color = "black"
                        self.canvas.create_rectangle(i - 1, j - 1, i + self.cell_size + 1, j + self.cell_size + 1,
                                                     fill=color)
                    self.grid[row_idx][col_idx] = 1
                else:
                    if self.grid[row_idx][col_idx] == 1:
                        color = "white"
                        self.canvas.create_rectangle(i - 1, j - 1, i + self.cell_size + 1, j + self.cell_size + 1,
                                                     fill=color)
                    self.grid[row_idx][col_idx] = 0

                if self.graphics:
                    self.root.update()

    def increase_entropy(self):
        if self.last_keypress + 0.5 < time.time():
            self.last_keypress = time.time()
            n_map = self.neighbours()
            self.next_generation(n_map)
            self.generation += 1
            self.label.set("Generation: " + str(self.generation))


def game_of_life(grid=None, graphics=True, make_steps=None, style=None):
    if grid is None:
        grid = numpy.zeros((20, 40))

    # read the file with parameters
    with open('GameParameters.json') as f:
        parameters = json.load(f)
    # set the parameters
    if make_steps is None:
        make_steps = parameters['configs']['make_steps']
    if style is None:
        cell_size = parameters['styles']['cell_size']
        line_width = parameters['styles']['line_width']
    
    if graphics:
        root = Tk()
        root.title('The game of life')
        canvas = Canvas(root, width=800, height=400)
        canvas.configure(background='white')
        for i in range(0, 800, cell_size + line_width):
            for j in range(0, 400, cell_size + line_width):
                canvas.create_line(i + cell_size + 1, j, i + cell_size + 1, j + cell_size + 1, fill="black")
                canvas.create_line(i, j + cell_size + 1, i + cell_size + 2, j + cell_size + 1, fill="black")

        def key(event):
            if event.char == ' ':
                grid_obj.increase_entropy()
            elif event.char == 'q':
                sys.exit()

        def callback(event):
            if grid[int(event.y / 20)][int(event.x / 20)] == 0:
                grid[int(event.y / 20)][int(event.x / 20)] = 1
                color = "black"
            else:
                grid[int(event.y / 20)][int(event.x / 20)] = 0
                color = "white"
            ii = (cell_size + line_width) * int(event.x / 20)
            jj = (cell_size + line_width) * int(event.y / 20)

            canvas.create_rectangle(ii - 1, jj - 1, ii + cell_size + 1, jj + cell_size + 1, fill=color)

        canvas.bind("<Key>", key)
        canvas.bind("<Button-1>", callback)
        var = StringVar()
        label = Label(root, textvariable=var, relief=RAISED, justify=LEFT)
        label.pack()
        var.set("Generation: 0")

        grid_obj = Grid(grid, (root, canvas, var), (cell_size, line_width))
    else:
        grid_obj = Grid(grid)

    # run the simulation
    if make_steps is not None:
        for i in range(make_steps):
            grid_obj.increase_entropy()

    if graphics:
        canvas.pack()
        canvas.focus_set()
        root.mainloop()

    return grid_obj.grid
