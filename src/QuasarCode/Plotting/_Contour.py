from typing import TYPE_CHECKING, Literal

from matplotlib.axes import Axes
if TYPE_CHECKING:
    from matplotlib.pylab import ArrayLike
from matplotlib.typing import ColorType
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.contour import QuadContourSet

from ..Data._Rect import Rect
from ._CachedPlotElements import CachedPlotContour

class Contour(object):

    def __init__(self, x_data: np.ndarray[tuple[int], np.dtype[np.floating]], y_data: np.ndarray[tuple[int], np.dtype[np.floating]], values: np.ndarray[tuple[int], np.dtype[np.floating]]|None = None) -> None:
        self.__can_compute: bool = True
        self.__x_data = x_data
        self.__y_data = y_data
        self.__values = values

        #self.__contour_levels: set[float] = set()
        self.__contour_levels: dict[float, list[ColorType, ArrayLike, Literal["solid", "dashed", "dashdot", "dotted"], float]] = {}

        self.__can_plot: bool = False
        self.__x_bin_locations: np.ndarray[tuple[int], np.dtype[np.floating]]|None = None
        self.__y_bin_locations: np.ndarray[tuple[int], np.dtype[np.floating]]|None = None
        self.__levels: np.ndarray[tuple[int, int], np.dtype[np.floating]]|None = None
        self.__cache_object = CachedPlotContour()
        self.__result: QuadContourSet|None = None

    def release_resources(self) -> None:
        if self.__can_compute:
            self.__can_compute = False
            del self.__x_data
            del self.__y_data
            del self.__values

    @property
    def data(self) -> CachedPlotContour:
        """
        Get the cache object for this contour.
        """
        return self.__cache_object

    @property
    def plotting_result(self) -> QuadContourSet|None:
        """
        Get the plotting result for this contour.
        """
        return self.__result

    @property
    def levels(self) -> np.ndarray[tuple[int, int], np.dtype[np.floating]]|None:
        return self.__levels

    @property
    def min_level(self) -> float|None:
        return self.__levels.min() if self.__levels is not None else None

    @property
    def max_level(self) -> float|None:
        return self.__levels.max() if self.__levels is not None else None

    @property
    def contour_levels(self) -> set[float]:
        return set(self.__contour_levels.keys())

    @property
    def contour_colours(self) -> tuple[ColorType, ...]:
        return tuple(self.__contour_levels[level][0] for level in sorted(self.__contour_levels.keys()))
    
    @property
    def contour_linewidths(self) -> tuple["ArrayLike", ...]:
        return tuple(self.__contour_levels[level][1] for level in sorted(self.__contour_levels.keys()))
    
    @property
    def contour_linestyles(self) -> tuple[Literal["solid", "dashed", "dashdot", "dotted"], ...]:
        return tuple(self.__contour_levels[level][2] for level in sorted(self.__contour_levels.keys()))
    
    @property
    def contour_alphas(self) -> tuple[float, ...]:
        return tuple(self.__contour_levels[level][3] for level in sorted(self.__contour_levels.keys()))
    
    def add_contours(self, *levels: float) -> None:
        for level in levels:
            if level not in self.__contour_levels:
                self.__contour_levels[level] = ["black", 1, "solid", 1.0]

    def remove_contours(self, *levels: float) -> None:
        for level in levels:
            if level in self.__contour_levels:
                del self.__contour_levels[level]
    
    def clear_contours(self) -> None:
        self.__contour_levels.clear()

    def set_colour(self, level: float, colour: ColorType) -> None:
        if level in self.__contour_levels:
            self.__contour_levels[level][0] = colour
        else:
            raise ValueError(f"Contour level {level} not found.")
        
    def set_linewidth(self, level: float, linewidth: "ArrayLike") -> None:
        if level in self.__contour_levels:
            self.__contour_levels[level][1] = linewidth
        else:
            raise ValueError(f"Contour level {level} not found.")
        
    def set_linestyle(self, level: float, linestyle: Literal["solid", "dashed", "dashdot", "dotted"]) -> None:
        if level in self.__contour_levels:
            self.__contour_levels[level][2] = linestyle
        else:
            raise ValueError(f"Contour level {level} not found.")

    def set_alpha(self, level: float, alpha: float) -> None:
        if level in self.__contour_levels:
            self.__contour_levels[level][3] = alpha
        else:
            raise ValueError(f"Contour level {level} not found.")

    def generate(self, gridsize = int|tuple[int,int], extent: Rect|None = None, **kwargs) -> None:
        if not self.__can_compute:
            raise RuntimeError("Cannot compute contours after resources have been released.")

        self.__levels, bin_x, bin_y = np.histogram2d(
            self.__x_data,
            self.__y_data,
            weights = self.__values,
            bins = gridsize,
            range = extent.range if extent is not None else None
        )

        self.__x_bin_locations = bin_x[:-1] + (bin_x[1] - bin_x[0]) / 2
        self.__y_bin_locations = bin_y[:-1] + (bin_y[1] - bin_y[0]) / 2

        self.__can_plot = True

    def plot(self, axis: Axes, **kwargs) -> QuadContourSet:
        if not self.__can_plot:
            raise RuntimeError("Cannot plot contours before calling \"generate\".")

        self.__result = axis.contour(
            self.__x_bin_locations,
            self.__y_bin_locations,
            self.__levels,
            levels = sorted(self.__contour_levels),
            linewidths = self.contour_linewidths,
            linestyles = self.contour_linestyles,
            alpha = self.contour_alphas,
            colors = self.contour_colours,
            **kwargs
        )

        self.__cache_object = CachedPlotContour.from_contours(self.__result, self.__x_bin_locations, self.__y_bin_locations, self.__levels)

        return self.__result
