from typing import Any, Literal

from matplotlib.figure import Figure
from matplotlib.axes import Axes

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
    relative_widths = AutoProperty[list[float]]()
    relative_heights = AutoProperty[list[float]]()
    vertical_spacing = AutoProperty_NonNullable[float](default_value = 0)
    horizontal_spacing = AutoProperty_NonNullable[float](default_value = 0)
    plots = AutoProperty_NonNullable[dict[str, CachedPlot]]()

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

    def add_row(self, number = 1, insert_at_index: int = -1) -> None:
        if number < 1:
            raise ValueError("Number of rows to add must be at least 1.")
        if self.__locked:
            raise RuntimeError("Cannot add rows after the figure has been created. Call `clear_axes` first.")
        for _ in range(number):
            self.mosaic.insert(insert_at_index, ["." for _ in range(self.columns)])
        self.rows += number

    def add_column(self, number = 1, insert_at_index: int = -1) -> None:
        if number < 1:
            raise ValueError("Number of columns to add must be at least 1.")
        if self.__locked:
            raise RuntimeError("Cannot add columns after the figure has been created. Call `clear_axes` first.")
        for row in self.mosaic:
            for _ in range(number):
                row.insert(insert_at_index, ".")
        self.columns += number

    def set_empty(self, row: int|list[int], column: int|list[int]) -> None:
        self.set_plot(".", row, column)

    def set_plot(self, name: str, row: int|list[int] = 0, column: int|list[int] = 0) -> None:
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

    def assign_plot(self, name: str, plot: CachedPlot) -> None:
        if not any([name in row for row in self.mosaic]):
            raise KeyError(f"No plot with the name \"{name}\" exists in the mosaic. Add the plot first with `set_plot`.")
        self.plots[name] = plot

    def unassign_plot(self, name: str) -> None:
        try:
            self.plots.pop(name)
        except KeyError: pass

    def clear_axes(self) -> None:
        if self.__locked:
            self.__figure = None
            self.__axes = None
            self.__locked = False

    def make_figure_and_axes(self, figure_kwargs: dict[str, Any]|None = None, mosaic_kwargs: dict[str, Any]|None = None, gridspec_kwargs: dict[str, Any]|None = None) -> tuple[Figure, dict[str, Axes]]:
        if self.__locked:
            raise RuntimeError("Figure and axes have already been created. Cannot create them again without first calling `clear_axes`.")
        self.__figure = Figure(figsize = self.figure_size, layout = self.layout, **(figure_kwargs if figure_kwargs is not None else {}))
        if self.title is not None:
            self.__figure.suptitle(self.title)
        self.__axes = self.__figure.subplot_mosaic(
            self.mosaic,
            width_ratios = self.relative_widths,
            height_ratios = self.relative_heights,
            gridspec_kw = { "wspace": self.horizontal_spacing, "hspace": self.vertical_spacing, **(gridspec_kwargs if gridspec_kwargs is not None else {}) },
            **(mosaic_kwargs if mosaic_kwargs is not None else {})
        )
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
            raise ValueError("Plot tag \".\" is reserved for empty plots. To use these axes, assign them a name first.")
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
