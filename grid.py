from __future__ import annotations
from layer_store import SetLayerStore, AdditiveLayerStore , SequenceLayerStore


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        Doc:
        The grid creates a list of list to store the layer values of the depending on
        the draw_style chosen

        Time complexity:
        O(n^2) as n is the size of one of the side of the grid and it is repeated
        2 times as for row x and y

        """
        # first we initialise the attributes of the grid with x,y,brush_size,drawstyle
        # and the grid
        self.x = x
        self.y = y
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE
        self.draw_style = draw_style
        self.grid = []
        for i in range(self.x):
            row = []
            for j in range(self.y):
                if draw_style == Grid.DRAW_STYLE_SET:
                    layer_store = SetLayerStore()
                elif draw_style == Grid.DRAW_STYLE_ADD:
                    layer_store = AdditiveLayerStore()
                elif draw_style == Grid.DRAW_STYLE_SEQUENCE:
                    layer_store = SequenceLayerStore()
                else:
                    raise ValueError(f"Invalid draw_style: {draw_style}")
                row.append(layer_store)
            self.grid.append(row)


    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        Doc:
        this increase the brush size by 1 and once hit the max which is 5 it will stop
        there and will not increase futher .

        Time complexity:
        O(1) as it is a simple increment

        """
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.


        Doc:
        this decrease the brush size by 1 and once hit the max which is 5 it will stop
        there and will not increase futher .

        Time complexity:
        O(1) as it is a simple increment

        """

        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        .get_top_layer()

        Doc :
        this code goes by x and y grid to apply the special if the layer is not none

        Time complexity:
        O(N^2) same as the grid it covers grid x and y and therefore it performs
        twice in given two rows
        """
        for i in range(self.x):
            for j in range(self.y):
                layer = self.grid[i][j]
                if layer is not None:
                    layer.special()


    def __getitem__(self, index):
        """Magic method to get the grid index """
        return self.grid[index]

