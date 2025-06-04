from typing import Any, Literal

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np

from ..Data._Rect import Rect
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable
from ._CachedPlotElements import CachedPlotElement, CachedPlotColourbar
from ._CachedPlot import CachedPlot

class CachedFigureGrid(CacheableStruct):
    title = AutoProperty[str](allow_uninitialised = True)
    mosaic = AutoProperty_NonNullable[list[list[str]]]()
    rows = AutoProperty_NonNullable[int](default_value = 1)
    columns = AutoProperty_NonNullable[int](default_value = 1)
    figure_size = AutoProperty_NonNullable[tuple[int, int]](default_value = (6, 8))
    layout = AutoProperty[Literal["constrained", "compressed", "tight"]](allow_uninitialised = True)
    relative_heights = AutoProperty[list[float]](allow_uninitialised = True)
    relative_widths = AutoProperty[list[float]](allow_uninitialised = True)
    vertical_spacing = AutoProperty_NonNullable[float](default_value = 0)
    horizontal_spacing = AutoProperty_NonNullable[float](default_value = 0)
    plots = AutoProperty_NonNullable[dict[str, CachedPlot]]()

    @property
    def physical_rect(self) -> Rect:
        return Rect.create_from_size(
            x = 0,
            y = 0,
            width = self.figure_size[0],
            height = self.figure_size[1]
        )

    @property
    def physical_heights(self) -> list[float]:
        total_height = self.figure_size[1]
        total_relative_height = sum(self.relative_heights) if self.relative_heights else self.rows
        return [total_height * (row_height / total_relative_height) for row_height in (self.relative_heights if self.relative_heights else [1] * self.rows)]
    
    @property
    def physical_widths(self) -> list[float]:
        total_width = self.figure_size[0]
        total_relative_width = sum(self.relative_widths) if self.relative_widths else self.columns
        return [total_width * (column_width / total_relative_width) for column_width in (self.relative_widths if self.relative_widths else [1] * self.columns)]

    def __init__(self, **kwargs):
        self.__figure: Figure|None = None
        self.__axes: dict[str, Axes]|None = None
        self.__locked = False
        mosaic_provided = "mosaic" in kwargs

        super().__init__(
            cacheable_attributes = ("title", "mosaic", "rows", "columns", "figure_size", "layout", "relative_widths", "relative_heights", "vertical_spacing", "horizontal_spacing", "plots"),
            **kwargs
        )

        if mosaic_provided:
            if len(self.mosaic) < 1 or len(self.mosaic[0]) < 1:
                raise ValueError("Mosaic must have at least one row and one column.")
            if any([len(row) != len(self.mosaic[0]) for row in self.mosaic]):
                raise ValueError("All rows in the mosaic must have the same number of columns.")

        if not mosaic_provided:
            self.mosaic = [["." for _ in range(self.columns)] for _ in range(self.rows)]
        else:
            self.rows = len(self.mosaic)
            self.columns = max(len(row) for row in self.mosaic)

        self.plots = {}

    def add_row(self, number = 1, insert_at_index: int = -1, height: float = 1.0, physical_height: bool = False, expand_figure: bool = False) -> None:
        if number < 1:
            raise ValueError("Number of rows to add must be at least 1.")
        if insert_at_index < 0:
            insert_at_index = self.rows + insert_at_index
        if self.__locked:
            raise RuntimeError("Cannot add rows after the figure has been created. Call `clear_axes` first.")
        if physical_height and not expand_figure:
            raise ValueError("Cannot add rows with physical height without expanding the figure. Set `expand_figure` to True.")
        if self.relative_heights is None:
            self.relative_heights = [1.0] * self.rows
        if physical_height:
            initial_physical_height = self.figure_size[1]
            if expand_figure:
                self.figure_size = (self.figure_size[0], self.figure_size[1] + height * number)
            height *= (sum(self.relative_heights) if self.relative_heights else self.rows) / initial_physical_height
        elif expand_figure:
            self.figure_size = (self.figure_size[0], self.figure_size[1] + (height * (self.figure_size[1] / sum(self.relative_heights))) * number)
        for _ in range(number):
            self.mosaic.insert(insert_at_index, ["." for _ in range(self.columns)])
            self.relative_heights.insert(insert_at_index, height)
        self.rows += number

    def add_column(self, number = 1, insert_at_index: int = -1, width: float = 1.0, physical_width: bool = False, expand_figure: bool = False) -> None:
        if number < 1:
            raise ValueError("Number of columns to add must be at least 1.")
        if insert_at_index < 0:
            insert_at_index = self.columns + insert_at_index
        if self.__locked:
            raise RuntimeError("Cannot add columns after the figure has been created. Call `clear_axes` first.")
        if physical_width and not expand_figure:
            raise ValueError("Cannot add columns with physical width without expanding the figure. Set `expand_figure` to True.")
        if self.relative_widths is None:
            self.relative_widths = [1.0] * self.columns
        if physical_width:
            initial_physical_width = self.figure_size[0]
            if expand_figure:
                self.figure_size = (self.figure_size[0] + width * number, self.figure_size[1])
            width *= (sum(self.relative_widths) if self.relative_widths else self.columns) / initial_physical_width
        elif expand_figure:
            self.figure_size = (self.figure_size[0] + (width * (self.figure_size[0] / sum(self.relative_widths))) * number, self.figure_size[1])
        for row in self.mosaic:
            for _ in range(number):
                row.insert(insert_at_index, ".")
        self.columns += number
        for _ in range(number):
            self.relative_widths.insert(insert_at_index, width)

    def resize_row(self, row: int|list[int], height: float, physical_height: bool = False, resize_figure: bool = False) -> None:
        if self.__locked:
            raise RuntimeError("Cannot resize rows after the figure has been created. Call `clear_axes` first.")
        if isinstance(row, int):
            row = [row]
        if self.relative_heights is None:
            self.relative_heights = [1.0] * self.rows
        initial_physical_figure_height = self.figure_size[1]
        initial_relative_figure_height = sum(self.relative_heights)
        new_relative_height = height * (self.figure_size[1] / initial_physical_figure_height) if physical_height else height
        old_relative_heights = []
        for i in row:
            if i >= self.rows or i < -self.rows:
                raise IndexError(f"Row index {i} is out of bounds for the number of rows ({self.rows}).")
            old_relative_heights.append(self.relative_heights[i])
            self.relative_heights[i] = new_relative_height
        if resize_figure:
            delta_physical_height = (new_relative_height * len(row) - sum(old_relative_heights)) * (initial_physical_figure_height / initial_relative_figure_height)
            self.figure_size = (self.figure_size[0], self.figure_size[1] + delta_physical_height)

    def resize_column(self, column: int|list[int], width: float, physical_width: bool = False, resize_figure: bool = False) -> None:
        if self.__locked:
            raise RuntimeError("Cannot resize columns after the figure has been created. Call `clear_axes` first.")
        if isinstance(column, int):
            column = [column]
        if self.relative_widths is None:
            self.relative_widths = [1.0] * self.columns
        initial_physical_figure_width = self.figure_size[0]
        initial_relative_figure_width = sum(self.relative_widths)
        new_relative_width = width * (self.figure_size[0] / initial_physical_figure_width) if physical_width else width
        old_relative_widths = []
        for j in column:
            if j >= self.columns or j < -self.columns:
                raise IndexError(f"Column index {j} is out of bounds for the number of columns ({self.columns}).")
            old_relative_widths.append(self.relative_widths[j])
            self.relative_widths[j] = new_relative_width
        if resize_figure:
            delta_physical_width = (new_relative_width * len(column) - sum(old_relative_widths)) * (initial_physical_figure_width / initial_relative_figure_width)
            self.figure_size = (self.figure_size[0] + delta_physical_width, self.figure_size[1])

    def assign_empty(self, row: int|list[int], column: int|list[int]) -> None:
        self.assign_plot(".", row, column)

    def assign_plot(self, name: str, row: int|list[int] = 0, column: int|list[int] = 0) -> None:
        if isinstance(row, int):
            row = [row]
        if isinstance(column, int):
            column = [column]
        for i in row:
            if i >= self.rows or i < -self.rows:
                raise IndexError(f"Row index {i} is out of bounds for the number of rows ({self.rows}).")
            for j in column:
                if j >= self.columns or j < -self.columns:
                    raise IndexError(f"Column index {j} is out of bounds for the number of columns ({self.columns}).")
                self.mosaic[i][j] = name

    def set_plot(self, name: str, plot: CachedPlot) -> None:
        if not any([name in row for row in self.mosaic]):
            raise KeyError(f"No plot with the name \"{name}\" exists in the mosaic. Add the plot first with `assign_plot`.")
        self.plots[name] = plot

    def remove_plot(self, name: str) -> None:
        try:
            self.plots.pop(name)
        except KeyError: pass

    def get_axis_rect_relative(self, name: str) -> Rect:
        if name == ".":
            raise ValueError("Plot tag \".\" is reserved for empty space. To use this space, assign a name first.")
        row_indexes, column_indexes = np.where(np.array(self.mosaic, dtype = str) == name)
        heights = (self.relative_heights if self.relative_heights else [1] * self.rows   )
        widths  = (self.relative_widths  if self.relative_widths  else [1] * self.columns)
        return Rect.create_from_size(
            x = sum(widths[:column_indexes[0]]),
            y = sum(heights[:row_indexes[0]]),
            width  = sum(widths[column_indexes[0] : column_indexes[-1] + 1]),
            height = sum(heights[row_indexes[0] : row_indexes[-1] + 1])
        )

    def get_axis_rect_physical(self, name: str) -> Rect:
        relative = self.get_axis_rect_relative(name)
        total_relative_height = sum(self.relative_heights) if self.relative_heights else self.rows
        total_relative_width = sum(self.relative_widths) if self.relative_widths else self.columns
        return Rect.create_from_size(
            x = (relative.x / total_relative_width) * self.figure_size[0],
            y = (relative.y / total_relative_height) * self.figure_size[1],
            width = (relative.width / total_relative_width) * self.figure_size[0],
            height = (relative.height / total_relative_height) * self.figure_size[1]
        )

    def clear_axes(self) -> None:
        if self.__locked:
            self.__figure = None
            self.__axes = None
            self.__locked = False

    def make_figure_and_axes(self, figure_kwargs: dict[str, Any]|None = None, mosaic_kwargs: dict[str, Any]|None = None, gridspec_kwargs: dict[str, Any]|None = None) -> tuple[Figure, dict[str, Axes]]:
        if self.__locked:
            raise RuntimeError("Figure and axes have already been created. Cannot create them again without first calling `clear_axes`.")
        self.__figure = plt.figure(figsize = self.figure_size, layout = self.layout, **(figure_kwargs if figure_kwargs is not None else {}))
        if self.title is not None:
            self.__figure.suptitle(self.title)
        self.__axes = self.__figure.subplot_mosaic(
            self.mosaic,
            width_ratios = self.relative_widths,
            height_ratios = self.relative_heights,
            gridspec_kw = { "wspace": self.horizontal_spacing, "hspace": self.vertical_spacing, **(gridspec_kwargs if gridspec_kwargs is not None else {}) },
            **(mosaic_kwargs if mosaic_kwargs is not None else {})
        )
        self.__locked = True
        return self.__figure, self.__axes
    
    @property
    def figure(self) -> Figure:
        if not self.__locked:
            raise RuntimeError("Figure has not been created yet. Call `make_figure_and_axes` first.")
        return self.__figure

    @property
    def axes(self) -> dict[str, Axes]:
        if not self.__locked:
            raise RuntimeError("Axes have not been created yet. Call `make_figure_and_axes` first.")
        return self.__axes
    
    def get_axis(self, plot_tag: str) -> Axes:
        if plot_tag == ".":
            raise ValueError("Plot tag \".\" is reserved for empty space. To use these axes, assign them a name first.")
        if not self.__locked:
            raise RuntimeError("Axes have not been created yet. Call `make_figure_and_axes` first.")
        if plot_tag not in self.__axes:
            raise KeyError(f"No axes found for plot tag \"{plot_tag}\".")
        return self.__axes[plot_tag]

    def render(self, forward_kwargs: dict[str, dict[str, dict[str, Any]]]|None = None, forward_colourbar_kwargs: dict[str, dict[str, dict[str, Any]]]|None = None) -> None:
        if not self.__locked:
            self.make_figure_and_axes()
        if forward_kwargs is None:
            forward_kwargs = {}
        if forward_colourbar_kwargs is None:
            forward_colourbar_kwargs = {}
        for plot_tag, plot in self.plots.items():
            plot.render(self.__figure, self.__axes[plot_tag], forward_kwargs = forward_kwargs.get(plot_tag, {}), forward_colourbar_kwargs = forward_colourbar_kwargs.get(plot_tag, {}))
