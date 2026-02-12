import os
from typing import Any, Literal, Optional

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np

from ..Data._Rect import Rect
from ..Tools._ScreenResolution import ScreenResolution
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable
from ._CachedPlotFontInfo import CachedPlotFontInfo
from ._CachedPlotCustomLegend import CachedPlotCustomLegend
from ._CachedPlotElements import CachedPlotColourbar
from ._CachedPlot import CachedPlot

class CachedFigureGrid(CacheableStruct):
    """
    Design a matplotlib figure using a mosaic layout.
    This (and any added cacheable plots) may be cached to disk.
    """

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
    colourbars = AutoProperty_NonNullable[dict[str, CachedPlotColourbar]]()
    custom_legends = AutoProperty_NonNullable[dict[str, CachedPlotCustomLegend]]()
    resolution = AutoProperty_NonNullable[int](default_value = 100)
    resolution_for_files = AutoProperty[int](allow_uninitialised = True)
    default_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    title_font = AutoProperty_NonNullable[CachedPlotFontInfo]()

    @property
    def physical_rect(self) -> Rect:
        """
        Rect -> Dimensions of the figure in inches.
        """
        return Rect.create_from_size(
            x = 0.0,
            y = 0.0,
            width = self.figure_size[0],
            height = self.figure_size[1]
        )

    @property
    def physical_heights(self) -> list[float]:
        """
        list[float] -> Height of each row in inches.
        """
        total_height = self.figure_size[1]
        total_relative_height = sum(self.relative_heights) if self.relative_heights else self.rows
        return [total_height * (row_height / total_relative_height) for row_height in (self.relative_heights if self.relative_heights else [1] * self.rows)]
    
    @property
    def physical_widths(self) -> list[float]:
        """
        list[float] -> Width of each column in inches.
        """
        total_width = self.figure_size[0]
        total_relative_width = sum(self.relative_widths) if self.relative_widths else self.columns
        return [total_width * (column_width / total_relative_width) for column_width in (self.relative_widths if self.relative_widths else [1] * self.columns)]

    def __init__(self, **kwargs) -> None:
        self.__figure: Figure|None = None
        self.__axes: dict[str, Axes]|None = None
        self.__locked = False
        mosaic_provided = "mosaic" in kwargs

        super().__init__(
            cacheable_attributes = ("title", "mosaic", "rows", "columns", "figure_size", "layout", "relative_widths", "relative_heights", "vertical_spacing", "horizontal_spacing", "plots", "resolution", "resolution_for_files"),
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
        self.colourbars = {}
        self.custom_legends = {}
        self.default_font = CachedPlotFontInfo()
        self.title_font = CachedPlotFontInfo()
        
    def set_resolution_custom(self, width_pixels: int|None = None, height_pixels: int|None = None, file_only: bool = False) -> None:
        """
        Set the resolution of the final image to fit within a custom width.

        Parameters:
            int width_pixels*:
                The desired width in pixels.
            int height_pixels*:
                The desired height in pixels.
            bool file_only:
                Apply this only to a saved image and not when displaying the image.

            * Only one of these parameters may be specified at a time!
        """
        if width_pixels is None and height_pixels is None:
            raise ValueError("At least one of `width_pixels` or `height_pixels` must be provided.")
        elif width_pixels is not None and height_pixels is not None:
            raise ValueError("Only one of `width_pixels` or `height_pixels` may be provided at a time.")
        resolution: int = int(width_pixels / self.figure_size[0]) if width_pixels is not None else int(height_pixels / self.figure_size[1])
        if file_only:
            self.resolution_for_files = resolution
        else:
            self.resolution = resolution
            if self.__figure is not None:
                self.__figure.dpi = resolution

    def set_resolution(self, resolution_spec: ScreenResolution, file_only: bool = False) -> None:
        """
        Set the resolution of the final image to fit within the specified screen resolution.

        NOTE: This applies to the CURRENT size of the figure. If the figure size changes, the
            resolution will remain fixed but the number of pixels used will increase/decrease!

        Parameters:
            bool file_only:
                Apply this only to a saved image and not when displaying the image.
        """
        resolution: int
        target_ratio = resolution_spec.value.height / resolution_spec.value.width
        plot_ratio = self.figure_size[1] / self.figure_size[0]
        if plot_ratio <= target_ratio:
            # The width is the limiting factor
            resolution = int(resolution_spec.value.width / self.figure_size[0])
        else:
            # The height is the limiting factor
            resolution = int(resolution_spec.value.height / self.figure_size[1])
        if file_only:
            self.resolution_for_files = resolution
        else:
            self.resolution = resolution
            if self.__figure is not None:
                self.__figure.dpi = resolution
        
    def set_resolution_720p(self, file_only: bool = False) -> None:
        """
        Set the resolution of the final image to fit within a 720p display.

        Parameters:
            bool file_only:
                Apply this only to a saved image and not when displaying the image.
        """
        self.set_resolution(ScreenResolution.get_720p(), file_only = file_only)

    def set_resolution_1080p(self, file_only: bool = False) -> None:
        """
        Set the resolution of the final image to fit within a 1080p display.

        Parameters:
            bool file_only:
                Apply this only to a saved image and not when displaying the image.
        """
        self.set_resolution(ScreenResolution.get_1080p(), file_only = file_only)

    def set_resolution_4K(self, file_only: bool = False) -> None:
        """
        Set the resolution of the final image to fit within a 4K display.

        Parameters:
            bool file_only:
                Apply this only to a saved image and not when displaying the image.
        """
        self.set_resolution(ScreenResolution.get_4K(), file_only = file_only)

    def set_resolution_8K(self, file_only: bool = False) -> None:
        """
        Set the resolution of the final image to fit within a 8K display.

        Parameters:
            bool file_only:
                Apply this only to a saved image and not when displaying the image.
        """
        self.set_resolution(ScreenResolution.get_8K(), file_only = file_only)

    def add_row(self, number: int = 1, insert_at_index: Optional[int] = None, height: float = 1.0, physical_height: bool = False, expand_figure: bool = False) -> None:
        """
        Add a new row of axes to the figure layout.

        Parameters:
            int number:
                Number of rows of this specification to add.
                Must be greater than or equal to 1.
                Default is  1.
            int insert_at_index:
                Index at which to insert the new rows.
                Default is -1, which means to append at the end.
            float height:
                Height of the new rows (relative unless specified as physical).
            bool physical_height:
                If True, the height is specified in inches.
                Note: this requires `expand_figure` to be True.
                Default is False.
            bool expand_figure:
                If True, the figure size will be expanded to accommodate the new rows.
                This is required when using `physical_height`.
                Default is False.
        """
        if number < 1:
            raise ValueError("Number of rows to add must be at least 1.")
        if insert_at_index is not None and insert_at_index < 0:
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
            if insert_at_index is not None:
                self.mosaic.insert(insert_at_index, ["." for _ in range(self.columns)])
                self.relative_heights.insert(insert_at_index, height)
            else:
                self.mosaic.append(["." for _ in range(self.columns)])
                self.relative_heights.append(height)
        self.rows += number

    def add_column(self, number: int = 1, insert_at_index: Optional[int] = None, width: float = 1.0, physical_width: bool = False, expand_figure: bool = False) -> None:
        """
        Add a new column of axes to the figure layout.

        Parameters:
            int number:
                Number of columns of this specification to add.
                Must be greater than or equal to 1.
                Default is  1.
            int insert_at_index:
                Index at which to insert the new columns.
                Default is None, which means to append at the end.
            float width:
                Width of the new columns (relative unless specified as physical).
            bool physical_width:
                If True, the width is specified in inches.
                Note: this requires `expand_figure` to be True.
                Default is False.
            bool expand_figure:
                If True, the figure size will be expanded to accommodate the new columns.
                This is required when using `physical_width`.
                Default is False.
        """
        if number < 1:
            raise ValueError("Number of columns to add must be at least 1.")
        if insert_at_index is not None and insert_at_index < 0:
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
                if insert_at_index is not None:
                    row.insert(insert_at_index, ".")
                else:
                    row.append(".")
        self.columns += number
        for _ in range(number):
            if insert_at_index is not None:
                self.relative_widths.insert(insert_at_index, width)
            else:
                self.relative_widths.append(width)

    def resize_row(self, row: int|list[int], height: float, physical_height: bool = False, resize_figure: bool = False) -> None:
        """
        Alter the height of one or more rows.

        Parameters:
            int|list[int] row:
                Index(es) of row(s) to set the height of.
            float height:
                Height of the new rows (relative unless specified as physical).
            bool physical_height:
                If True, the height is specified in inches.
                Note: this requires `expand_figure` to be True.
                Default is False.
            bool expand_figure:
                If True, the figure size will be expanded to accommodate the new rows.
                This is required when using `physical_height`.
                Default is False.
        """
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
        """
        Alter the width of one or more columns.

        Parameters:
            int|list[int] column:
                Index(es) of column(s) to set the width of.
            float width:
                Width of the new columns (relative unless specified as physical).
            bool physical_width:
                If True, the width is specified in inches.
                Note: this requires `expand_figure` to be True.
                Default is False.
            bool expand_figure:
                If True, the figure size will be expanded to accommodate the new columns.
                This is required when using `physical_width`.
                Default is False.
        """
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
        """
        Assign one or more grid elements to be empty space.
        This functions as a wrapper for `assign_plot` with the name ".".

        Parameters:
            int|list[int] row:
                Index(es) of row(s) to assign as empty.
            int|list[int] column:
                Index(es) of column(s) to assign as empty.
        """
        self.assign_plot(".", row, column)

    def assign_plot(self, name: str, row: int|list[int] = 0, column: int|list[int] = 0) -> None:
        """
        Assign one or more grid elements to an axis name.
        Row and column indexes should be sequential to avoid gaps.

        Parameters:
            int|list[int] row:
                Index(es) of row(s) to assign this name.
            int|list[int] column:
                Index(es) of column(s) to assign this name.
        """
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
        """
        Link an axis name in the figure layout with a CachedPlot instance for easy rendering.

        Parameters:
            str name:
                Name of the axis to link.
            CachedPlot plot:
                CachedPlot instance to insert.
        """
        if not any([name in row for row in self.mosaic]):
            raise KeyError(f"No plot with the name \"{name}\" exists in the mosaic. Add the plot first with `assign_plot`.")
        self.plots[name] = plot

    def remove_plot(self, name: str) -> None:
        """
        Remove an added CachedPlot instance.

        Parameters:
            str name:
                Name of the axis to unlink.
        """
        try:
            self.plots.pop(name)
        except KeyError: pass

    def set_colourbar(self, name: str, colourbar: CachedPlotColourbar, target_plot: str, target_element: str) -> None:
        """
        Link an axis name in the figure layout with a CachedPlotColourbar instance for easy rendering.
        Note: this circumvents the need to create a separate CachedPlot instance to host the colourbar.
        Adding colourbars into the layout mosaic is recommended as this allows greater control over the sizes of individual plots.

        Parameters:
            str name:
                Name of the axis to link.
            CachedPlotColourbar colourbar:
                CachedPlotColourbar instance to insert.
        """
        if name in self.colourbars:
            raise KeyError(f"A colourbar already exists with the name \"{name}\".")
        if not any([name in row for row in self.mosaic]):
            raise KeyError(f"No plot with the name \"{name}\" exists in the mosaic. Add the plot first with `assign_plot`.")
        if not any([target_plot in row for row in self.mosaic]):
            raise KeyError(f"No plot with the name \"{target_plot}\" exists in the mosaic. Add the plot first with `assign_plot`.")
        colourbar.target_element = target_element
        colourbar.target_plot = target_plot
        colourbar.add_to_axis = False
        self.colourbars[name] = colourbar
        
    def remove_colourbar(self, name: str) -> None:
        """
        Remove an added CachedPlotColourbar instance.

        Parameters:
            str name:
                Name of the axis to unlink.
        """
        try:
            self.colourbars.pop(name)
        except KeyError: pass

    def get_axis_rect_relative(self, name: str) -> Rect:
        """
        Get a Rect instance containing the relative position and size of a named axis.

        Parameters:
            str name:
                Name of the axis.

        Returns:
            Rect: Relative coordinates of the bottom-left corner and dimensions.
        """
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
        """
        Get a Rect instance containing the position and size in inches of a named axis.

        Parameters:
            str name:
                Name of the axis.

        Returns:
            Rect: Coordinates of the bottom-left corner and dimensions.
        """
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
        """
        Delete the figure and axes objects created by `make_figure_and_axes`.
        This will unlock the instance and allow further alteration of the layout.
        """
        if self.__locked:
            self.__figure = None
            self.__axes = None
            self.__locked = False

    def make_figure_and_axes(self, figure_kwargs: dict[str, Any]|None = None, mosaic_kwargs: dict[str, Any]|None = None, gridspec_kwargs: dict[str, Any]|None = None) -> tuple[Figure, dict[str, Axes]]:
        """
        Generate matplotlib figure and axes objects according to the layout specification.
        Doing so will lock the object's state and prevent further alterations to the layout.
        These may be subsequently accessed through the `figure` and `axes` properties.

        Parameters:
            dict[str, Any] figure_kwargs:
                Additional keyword arguments to pass to `plt.figure`.
                `figsize`, `layout`, and `dpi` are already set and MUST not be specified here.
            dict[str, Any] mosaic_kwargs:
                Additional keyword arguments to pass to `plt.subplot_mosaic`.
                `width_ratios` and `height_ratios` are already set and MUST not be specified here.
                `gridspec_kw` may be altered using the `gridspec_kwargs` parameter.
            dict[str, Any] gridspec_kwargs:
                Additional keyword arguments to pass to the gridspec constructor.
                `wspace` and `hspace` are already set and MUST not be specified here.

        Returns:
            tuple[Figure, dict[str, Axes]]:
                The created figure and a dictionary of axes keyed by their names.
        """
        if self.__locked:
            raise RuntimeError("Figure and axes have already been created. Cannot create them again without first calling `clear_axes`.")
        self.__figure = plt.figure(figsize = self.figure_size, layout = self.layout, **(figure_kwargs if figure_kwargs is not None else {}))
        self.__figure.dpi = self.resolution
        if self.title is not None:
            self.__figure.suptitle(self.title, **self.title_font.with_default(self.default_font).fontdict)
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
        """
        Figure -> The matplotlib figure object created by `make_figure_and_axes`.

        Raises:
            RuntimeError: If the figure has not been created yet.
        """
        if not self.__locked:
            raise RuntimeError("Figure has not been created yet. Call `make_figure_and_axes` first.")
        return self.__figure

    @property
    def axes(self) -> dict[str, Axes]:
        """
        Axes -> The dictionary of axes created by `make_figure_and_axes`.

        Raises:
            RuntimeError: If the figure has not been created yet.
        """
        if not self.__locked:
            raise RuntimeError("Axes have not been created yet. Call `make_figure_and_axes` first.")
        return self.__axes
    
    def get_axis(self, plot_tag: str) -> Axes:
        """
        Get the axes associated with a specific plot tag.

        Parameters:
            str plot_tag:
                The name of the plot to retrieve the axes for.

        Returns:
            Axes: The axes object associated with the specified plot tag.
        """
        if plot_tag == ".":
            raise ValueError("Plot tag \".\" is reserved for empty space. To use these axes, assign them a name first.")
        if not self.__locked:
            raise RuntimeError("Axes have not been created yet. Call `make_figure_and_axes` first.")
        if plot_tag not in self.__axes:
            raise KeyError(f"No axes found for plot tag \"{plot_tag}\".")
        return self.__axes[plot_tag]

    def render(self, forward_kwargs: dict[str, dict[str, dict[str, Any]]]|None = None, forward_colourbar_kwargs: dict[str, dict[str, dict[str, Any]]]|None = None) -> None:
        """
        Automatically render any associated CachedPlot instances onto their axes.
        If `make_figure_and_axes` has not been called, this will be done automatically. If you wish to control other elements of figure and axis creation, call that method first.

        Parameters:
            dict[str, dict[str, dict[str, Any]]] forward_kwargs:
                A dictionary of keyword arguments to pass to each plot's `render` method. Keys are the names of each axis.
            dict[str, dict[str, dict[str, Any]]] forward_colourbar_kwargs:
                A dictionary of keyword arguments to pass to each plot's `render` method for the colourbar. Keys are the names of each axis.
        """
        if not self.__locked:
            self.make_figure_and_axes()
        if forward_kwargs is None:
            forward_kwargs = {}
        if forward_colourbar_kwargs is None:
            forward_colourbar_kwargs = {}
        for plot_tag, plot in self.plots.items():
            plot.render(self.__figure, self.__axes[plot_tag], figure_default_font = self.default_font, forward_kwargs = forward_kwargs.get(plot_tag, {}), forward_colourbar_kwargs = forward_colourbar_kwargs.get(plot_tag, {}))
        for plot_tag, colourbar in self.colourbars.items():
            colourbar.render(self.__figure, self.__axes[plot_tag], self.plots[colourbar.target_plot].plot_elements[colourbar.target_element]._result, default_font = self.default_font, **forward_colourbar_kwargs.get(plot_tag, {}))
        for legend in self.custom_legends.values():
            legend.render(self.__figure, None, default_font = self.default_font, elements_by_figure_plot = { plot_tag : plot.plot_elements for plot_tag, plot in self.plots.items() })

    def save_png(self, filename: str, directory: str|None = None, **kwargs) -> None:
        """
        Save the figure as a PNG file with the specified resolution.
        The resolution for the file may be set differently to the display resolution using `resolution_for_files`.

        Parameters:
            str filename:
                The name of the file to save the figure as (without extension).
            str|None directory:
                The directory to save the file in. If None, the current working directory is used.
        """
        filepath = f"{filename}.png"
        if directory is not None:
            filepath = os.path.join(directory, filepath)
        if not self.__locked:
            raise RuntimeError("Figure has not been created yet. Call `make_figure_and_axes` first.")
        if "dpi" in kwargs:
            kwargs["dpi"] = self.resolution_for_files if self.resolution_for_files is not None else self.resolution
        self.__figure.savefig(filepath, **kwargs)
    def save_jpeg(self, filename: str, directory: str|None = None, **kwargs) -> None:
        """
        Save the figure as a JPEG file with the specified resolution.
        The resolution for the file may be set differently to the display resolution using `resolution_for_files`.

        Parameters:
            str filename:
                The name of the file to save the figure as (without extension).
            str|None directory:
                The directory to save the file in. If None, the current working directory is used.
        """
        filepath = f"{filename}.jpeg"
        if directory is not None:
            filepath = os.path.join(directory, filepath)
        if not self.__locked:
            raise RuntimeError("Figure has not been created yet. Call `make_figure_and_axes` first.")
        if "dpi" in kwargs:
            kwargs["dpi"] = self.resolution_for_files if self.resolution_for_files is not None else self.resolution
        self.__figure.savefig(filepath, **kwargs)
    def save_pdf(self, filename: str, directory: str|None = None, **kwargs) -> None:
        """
        Save the figure as a PDF file with the specified resolution.
        The resolution for the file may be set differently to the display resolution using `resolution_for_files`.

        Parameters:
            str filename:
                The name of the file to save the figure as (without extension).
            str|None directory:
                The directory to save the file in. If None, the current working directory is used.
        """
        filepath = f"{filename}.pdf"
        if directory is not None:
            filepath = os.path.join(directory, filepath)
        if not self.__locked:
            raise RuntimeError("Figure has not been created yet. Call `make_figure_and_axes` first.")
        if "dpi" in kwargs:
            kwargs["dpi"] = self.resolution_for_files if self.resolution_for_files is not None else self.resolution
        if self.layout == "tight":
            kwargs["bbox_inches"] = "tight"
        self.__figure.savefig(filepath, **kwargs)
    def save_svg(self, filename: str, directory: str|None = None, **kwargs) -> None:
        """
        Save the figure as a SVG (Simple Vector Graphic) file with the specified resolution.
        The resolution for the file may be set differently to the display resolution using `resolution_for_files`.

        Parameters:
            str filename:
                The name of the file to save the figure as (without extension).
            str|None directory:
                The directory to save the file in. If None, the current working directory is used.
        """
        filepath = f"{filename}.svg"
        if directory is not None:
            filepath = os.path.join(directory, filepath)
        if not self.__locked:
            raise RuntimeError("Figure has not been created yet. Call `make_figure_and_axes` first.")
        if "dpi" in kwargs:
            kwargs["dpi"] = self.resolution_for_files if self.resolution_for_files is not None else self.resolution
        self.__figure.savefig(filepath, **kwargs)
