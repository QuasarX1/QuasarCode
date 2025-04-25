from collections.abc import Callable
from functools import wraps
from typing import TypeVar, TypeAlias, Literal

from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.axes import Axes
from matplotlib.colors import Colormap
from matplotlib.typing import ColorType
import numpy as np

from ..Data._Rect import Rect
from ._CachedPlotElements import CachedPlotHexbin

COLOUR_FUNCTION_TYPE: TypeAlias = Callable[[float|None, float|None, float|None], Callable[[np.ndarray[tuple[int], np.dtype[np.integer]]], float]]

class Hexbin(object):

    COLOUR_FUNCTION_TYPE = COLOUR_FUNCTION_TYPE
    
    def __init__(
        self,
        x_data: np.ndarray[tuple[int], np.dtype[np.floating]],
        y_data: np.ndarray[tuple[int], np.dtype[np.floating]],
        colour_function: COLOUR_FUNCTION_TYPE = None,
        cache: CachedPlotHexbin|None = None
    ) -> None:
        super().__init__()
        self.__x_data = x_data
        self.__y_data = y_data
        self.__colour_function = colour_function if colour_function is not None else Hexbin.create_hexbin_count()
        self.__cache_object = cache if cache is not None else CachedPlotHexbin()

    @property
    def colour_function(self) -> COLOUR_FUNCTION_TYPE: # type: ignore[valid-type]
        """
        The function used to generate another function for calculating the colour of the hexbin cells.
        """
        return self.__colour_function

    @property
    def data(self) -> CachedPlotHexbin:
        """
        Get the cache object for this hexbin.
        """
        return self.__cache_object
    
    def plot_hexbin(
        self,
        default_bin_value: float = -np.inf,
        extent: Rect|None = None,
        gridsize: int|tuple[int, int]|None = None,
        colourmap: str|Colormap|None = None,
        min_value: float|None = None,
        max_value: float|None = None,
        edge_colour: ColorType|Literal["face", "none"]|None = None,
        alpha_values: np.ndarray[tuple[int], np.dtype[np.floating]]|None = None,
        axis: Axes|None = None,
        **hexbin_kwargs
    ) -> PolyCollection:
        """
        Plot a hexbin using a pre-defined colour scheme.

        hexbin_kwargs will be passed to the `plt.hexbin` function call (or that of the provided axis).

        May raise ValueError if any of the arguments not provided are not set on the data object.
        """

        extent = extent if extent is not None else self.data.extent
        gridsize = gridsize if gridsize is not None else self.data.gridsize
        colourmap = colourmap if colourmap is not None else self.data.colourmap
        min_value = min_value if min_value is not None else self.data.min_value
        max_value = max_value if max_value is not None else self.data.max_value
        edge_colour = edge_colour if edge_colour is not None else self.data.edgecolour
        alpha_values = alpha_values if alpha_values is not None else self.data.bin_alphas

        hexes = (axis if axis is not None else plt).hexbin(
            x = self.__x_data,
            y = self.__y_data,
            C = np.arange(len(self.__x_data)),
            reduce_C_function = self.__colour_function(min_value, max_value, default_bin_value),
            extent = extent.extent,
            gridsize = gridsize,
            cmap = colourmap,
            vmin = min_value,
            vmax = max_value,
            edgecolor = edge_colour,
            **hexbin_kwargs
        )

        if alpha_values is not None:
            hexes.set_alpha(alpha_values)

        self.__cache_object = CachedPlotHexbin.from_hexes(hexes, extent, gridsize, min_value, max_value, edgecolours_match_faces = edge_colour == "face")

        return hexes



    @staticmethod
    def create_hexbin_colour_function(statistic: Callable[[np.ndarray[tuple[int], np.dtype[np.integer]]], float]):
        """
        Create a function for calculating the value for colour mapping of hexbin cells.

        The return value of this function can be passed to `plot_hexbin` as an argument for the parameter `colour_function`.
        """

        def ready_hexbin_colour_function(min_value: float|None = None, max_value: float|None = None, default_bin_value: float = -np.inf):

            @wraps(statistic)
            def calculate_bin_colour(indices: np.ndarray, /) -> float:
                if len(indices) == 0:
                    return default_bin_value
                try:
                    result = statistic(indices)
                except Exception:
                    return default_bin_value
                if min_value is not None and result < min_value:
                    return min_value
                elif max_value is not None and result > max_value:
                    return max_value
                else:
                    return result

            return calculate_bin_colour
        
        return ready_hexbin_colour_function



    @staticmethod
    def create_hexbin_count():
        """
        Assign hexbin cell colour to the number of elements that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_count(indices: np.ndarray, /) -> float:
            return len(indices)
        return calculate_statistic_count



    @staticmethod
    def create_hexbin_log10_count():
        """
        Assign hexbin cell colour to the log_10 of the number of elements that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_log10_count(indices: np.ndarray, /) -> float:
            return np.log10(len(indices))
        return calculate_statistic_log10_count



    @staticmethod
    def create_hexbin_fraction(mask: np.ndarray[tuple[int], np.dtype[np.bool_]]):
        """
        Assign hexbin cell colour to the fraction of of elements that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_fraction(indices: np.ndarray, /) -> float:
            return mask[indices].sum() / len(indices)
        return calculate_statistic_fraction



    @staticmethod
    def create_hexbin_quantity_fraction(data: np.ndarray[tuple[int], np.dtype[np.floating]], mask: np.ndarray[tuple[int], np.dtype[np.bool_]]):
        """
        Assign hexbin cell colour to the fraction of of elements that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_quantity_fraction(indices: np.ndarray, /) -> float:
            subset = data[indices]
            return subset[mask[indices]].sum() / subset.sum()
        return calculate_statistic_quantity_fraction



    @staticmethod
    def create_hexbin_sum(data: np.ndarray):
        """
        Assign hexbin cell colour to the sum of the elements from this dataset that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_sum(indices: np.ndarray, /) -> float:
            return data[indices].sum()
        return calculate_statistic_sum



    @staticmethod
    def create_hexbin_log10_sum(data: np.ndarray):
        """
        Assign hexbin cell colour to the log_10 of the sum of the elements from this dataset that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_log10_sum(indices: np.ndarray, /) -> float:
            return np.log10(data[indices].sum())
        return calculate_statistic_log10_sum



    @staticmethod
    def create_hexbin_sum_log10(data: np.ndarray):
        """
        Assign hexbin cell colour to the sum of log_10 of the the elements from this dataset that fall within the bin.

        Note, it is advised you use `create_hexbin_sum` and pass the `np.log10(data)` to it instead of using this function, unless retaining a second copy of the data array is problematic.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_sum_log10(indices: np.ndarray, /) -> float:
            return np.log10(data[indices]).sum()
        return calculate_statistic_sum_log10



    @staticmethod
    def create_hexbin_mean(data: np.ndarray, offset: float = 0.0):
        """
        Assign hexbin cell colour to the mean of elements from this dataset that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_mean(indices: np.ndarray, /) -> float:
            return np.mean(data[indices]) + offset
        return calculate_statistic_mean



    @staticmethod
    def create_hexbin_log10_mean(data: np.ndarray, offset: float = 0.0):
        """
        Assign hexbin cell colour to the mean of elements from this dataset that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_log10_mean(indices: np.ndarray, /) -> float:
            return np.log10(np.mean(data[indices])) + offset
        return calculate_statistic_log10_mean



    @staticmethod
    def create_hexbin_weighted_mean(data: np.ndarray, weights: np.ndarray, offset: float = 0.0):
        """
        Assign hexbin cell colour to the mean of elements from this dataset that fall within the bin.

        Use the weights from an array of equal length.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_weighted_mean(indices: np.ndarray, /) -> float:
            return np.average(data[indices], weights = weights[indices]) + offset
        return calculate_statistic_weighted_mean



    @staticmethod
    def create_hexbin_log10_weighted_mean(data: np.ndarray, weights: np.ndarray, offset: float = 0.0):
        """
        Assign hexbin cell colour to the mean of elements from this dataset that fall within the bin.

        Use the weights from an array of equal length.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_log10_weighted_mean(indices: np.ndarray, /) -> float:
            return np.log10(np.average(data[indices], weights = weights[indices])) + offset
        return calculate_statistic_log10_weighted_mean



    @staticmethod
    def create_hexbin_median(data: np.ndarray):
        """
        Assign hexbin cell colour to the median of elements from this dataset that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_median(indices: np.ndarray, /) -> float:
            return np.median(data[indices])
        return calculate_statistic_median



    @staticmethod
    def create_hexbin_percentile(data: np.ndarray, percentile: float):
        """
        Assign hexbin cell colour to the specified percentile of elements from this dataset that fall within the bin.
        """
        @Hexbin.create_hexbin_colour_function
        def calculate_statistic_percentile(indices: np.ndarray, /) -> float:
            return np.percentile(data[indices], percentile)
        return calculate_statistic_percentile
