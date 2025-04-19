from collections.abc import Callable, Sequence
from functools import wraps
from typing import cast as typing_cast, Any, TypeVar

from matplotlib import pyplot as plt, _preprocess_data
from matplotlib.axes import Axes
from matplotlib.collections import PolyCollection
from matplotlib.colors import Colormap
from matplotlib.typing import ColorType
from matplotlib._docstring import dedent_interpd
import numpy as np

from .._global_settings import settings_object as Settings
from ..MPI import mpi_sum, mpi_mean, mpi_gather_array



T = TypeVar("T")

class HexbinRenderer(object):
    """
    Automate the creation of matplotlib hexbin plots using custom bin value calculations.

    MPI support available, however bin value and alpha functions are expected to handle MPI
    communication internally before returning the same bin value accross all ranks! Built-in
    methods have support for this.
    """

    def __init__(
        self,
        bin_statistic:     Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]|None = None,
        bin_value_min:     float|None          = None,
        bin_value_max:     float|None          = None,
        bin_value_default: float               = -np.inf,
        cmap:              str|Colormap|None   = "viridis",
        gridsize:          int|tuple[int, int] = 100,
        edgecolor:         ColorType|None      = None,
    ) -> None:
        
        self.__hexes: PolyCollection|None = None

        self.__bin_statistic = bin_statistic if bin_statistic is not None else HexbinRenderer.bin_statistic_count
        self.__create_bin_function = HexbinRenderer._create_hexbin_colour_function(self.__bin_statistic)
        self.__bin_min = bin_value_min
        self.__bin_max = bin_value_max
        self.__bin_default = bin_value_default

        self.__cmap = cmap
        self.__gridsize = gridsize
        self.__edgecolor = edgecolor

        self.__alpha_global:                 float|None = None
        self.__alpha_values:                 np.ndarray[tuple[int], np.dtype[np.float16]]|None = None
        self.__alpha_calculator:             Callable[[float, float, float, float], Callable[[float, np.ndarray[tuple[int], np.dtype[np.int64]]], float]]|None = None
        self.__alpha_calculator_min_return:  float|None = None
        self.__alpha_calculator_max_return:  float|None = None
        self.__alpha_calculator_min:         float|None = None
        self.__alpha_calculator_cap:         float|None = None
        self.__alpha_calculator_use_unbound: float|None = None

    @property
    def hexes(self) -> PolyCollection|None:
        """
        `PolyCollection|None` Result of calling matplotlib hexbin method.

        This is only set after the renderer has been plotted for the first time.
        """
        return self.__hexes

    @property
    def bin_value_min(self) -> float|None:
        """
        `float|None` Configured minimum value a bin may be assigned.
        """
        return self.__bin_min
    @bin_value_min.setter
    def bin_value_min(self, value: float|None) -> None:
        """
        `float|None` Configured minimum value a bin may be assigned.
        """
        self.__bin_min = value

    @property
    def bin_value_max(self) -> float|None:
        """
        `float|None` Configured maximum value a bin may be assigned.
        """
        return self.__bin_max
    @bin_value_max.setter
    def bin_value_max(self, value: float|None) -> None:
        """
        `float|None` Configured maximum value a bin may be assigned.
        """
        self.__bin_max = value

    @property
    def bin_value_default(self) -> float:
        """
        `float` Configured default value a bin is assigned when empty.
        """
        return self.__bin_default
    @bin_value_default.setter
    def bin_value_default(self, value: float) -> None:
        """
        `float` Configured default value a bin is assigned when empty.
        """
        self.__bin_default = value

    @property
    def bin_alpha_floor(self) -> float:
        """
        `float` Configured minimum alpha a bin may be assigned. Below this, bins are transparent
        (alpha = 0).

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        return typing_cast(float, self.__alpha_calculator_min)
    @bin_alpha_floor.setter
    def bin_alpha_floor(self, value: float) -> None:
        """
        `float` Configured minimum alpha a bin may be assigned. Below this, bins are transparent
        (alpha = 0).

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        self.__alpha_calculator_min = value

    @property
    def bin_alpha_cap(self) -> float:
        """
        `float` Configured maximum alpha a bin may be assigned. Above this, bins are capped at this
        value.

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        return typing_cast(float, self.__alpha_calculator_cap)
    @bin_alpha_cap.setter
    def bin_alpha_cap(self, value: float) -> None:
        """
        `float` Configured maximum alpha a bin may be assigned. Above this, bins are capped at this
        value.

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        self.__alpha_calculator_cap = value

    @property
    def bin_alpha_value_min(self) -> float:
        """
        `float` Configured return value from the alpha calculation function that should be mapped
        to an alpha of 0 (transparent).

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        return typing_cast(float, self.__alpha_calculator_min_return)
    @bin_alpha_value_min.setter
    def bin_alpha_value_min(self, value: float) -> None:
        """
        `float` Configured return value from the alpha calculation function that should be mapped
        to an alpha of 0 (transparent).

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        self.__alpha_calculator_min_return = value

    @property
    def bin_alpha_value_max(self) -> float:
        """
        `float` Configured return value from the alpha calculation function that should be mapped
        to an alpha of 1 (opaque).

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        return typing_cast(float, self.__alpha_calculator_max_return)
    @bin_alpha_value_max.setter
    def bin_alpha_value_max(self, value: float) -> None:
        """
        `float` Configured return value from the alpha calculation function that should be mapped
        to an alpha of 1 (opaque).

        Raises a `NotImplementedError` if alpha is not configured to be dynamic.
        """
        if self.__alpha_calculator is None:
            raise NotImplementedError("Alpha is not dynamic. Call `set_alpha_dynamic` first.")
        self.__alpha_calculator_max_return = value

    def set_alpha_all_bins(self, alpha: float) -> None:
        """
        Set the alpha of all hexes.

        Parameters:
            `float|None` alpha:
                The alpha value to use in the range [0 -> 1].
                Set to `None` to clear any alpha related configuration.

        See also:
            `set_alpha_per_bin`
            `set_alpha_dynamic`
        """
        if alpha is not None and (alpha < 0 or alpha > 1):
            raise ValueError("Alpha value outside the range [0 -> 1].")
        self.__alpha_global                 = alpha
        self.__alpha_values                 = None
        self.__alpha_calculator             = None
        self.__alpha_calculator_min_return  = None
        self.__alpha_calculator_max_return  = None
        self.__alpha_calculator_min         = None
        self.__alpha_calculator_cap         = None
        self.__alpha_calculator_use_unbound = None

    def set_alpha_per_bin(self, alpha_values: np.ndarray[tuple[int], np.dtype[np.float16]]) -> None:
        """
        Set the alpha of each hex individually.

        Parameters:
            `float|None` alpha:
                The alpha value to use in the range [0 -> 1].
                Set to `None` to clear any alpha related configuration.

        See also:
            `set_alpha_per_bin`
            `set_alpha_dynamic`
        """
        is_invalid = (alpha_values < 0) | (alpha_values > 1)
        if is_invalid.any():
            raise ValueError("One or more alpha value(s) outside the range [0 -> 1].")
        self.__alpha_global                 = None
        self.__alpha_values                 = alpha_values.astype(np.float16)
        self.__alpha_calculator             = None
        self.__alpha_calculator_min_return  = None
        self.__alpha_calculator_max_return  = None
        self.__alpha_calculator_min         = None
        self.__alpha_calculator_cap         = None
        self.__alpha_calculator_use_unbound = None

    def set_alpha_dynamic(
        self,
        alpha_function:                       Callable[[float, np.ndarray[tuple[int], np.dtype[np.int64]]], float],
        alpha_function_min:                   float = 0.0,
        alpha_function_max:                   float = 1.0,
        alpha_min:                            float = 0.0,
        alpha_max:                            float = 1.0,
        calculation_uses_unbounded_bin_value: bool  = False
    ) -> None:
        """
        Set the alpha of an individual hex according to its value.

        Values of alpha need to be a float in the range [0 -> 1]. While the return value(s) of
        `alpha_function` may return values outside of this range, the following parameters should
        be used to control how the results of `alpha_function` are mapped to this range:

            `alpha_function_min` and `alpha_function_max` maps the range of return values between 0
            and 1 (inclusive) using the minimum and maximum values respectively.

            `alpha_min` limits what the minimum alpha value is that should actually be displayed.

            `alpha_max` caps the maximum alpha value with larger values capped at this value.

        When using MPI, alpha calculation functions that rely on the array of indexes MUST
        implement their own MPI support!

        Parameters:
            `Callable[[float, numpy.ndarray[(I,), numpy.int64]], float]` alpha_function:
                Function that calculates the value of alpha for a single bin.
                Takes two parameters: the computed value of the bin and the indexes of data
                elements that fall within the bin. Returns a single float value.
                Returned values ought to be in the range [0 -> 1] unless `alpha_function_min` and
                `alpha_function_max` are set.
            (optional) `float` alpha_function_min:
                Minimum return value that should be mapped to an alpha of 0 (invisible).
                Default is `0.0`.
            (optional) `float` alpha_function_max:
                Maximum return value that should be mapped to an alpha of 1 (opaque).
                Default is `1.0`.
            (optional) `float` alpha_min:
                Minimum alpha value to display. Values below this are invisible (alpha = 0).
                Must be in the range [0 -> 1) and less than `alpha_max`.
                Default is `0.0`.
            (optional) `float` alpha_max:
                Maximum alpha value to display. Values above this are capped at this value.
                Must be in the range (0 -> 1] and greater than `alpha_min`.
                Default is `1.0`.
            (optional) `bool` calculation_uses_unbounded_bin_value:
                Should the calculation of alpha use the calculated bin value before or after
                enforcement of any limits.
                Default is `False`.

        See also:
            `set_alpha_all_bins`
            `set_alpha_per_bin`
        """

        if alpha_min < 0:
            raise ValueError(f"Argument for \"alpha_min\" ({alpha_min}) less than 0.")
        if alpha_max > 1:
            raise ValueError(f"Argument for \"alpha_max\" ({alpha_max}) greater than 1.")
        if alpha_max <= alpha_min:
            raise ValueError(f"Argument for \"alpha_min\" ({alpha_min}) greater than argument for \"alpha_max\" ({alpha_max}).")

        self.__alpha_global                 = None
        self.__alpha_values                 = None
        self.__alpha_calculator             = HexbinRenderer._create_hexbin_alpha_function(alpha_function)
        self.__alpha_calculator_min_return  = alpha_function_min
        self.__alpha_calculator_max_return  = alpha_function_max
        self.__alpha_calculator_min         = alpha_min
        self.__alpha_calculator_cap         = alpha_max
        self.__alpha_calculator_use_unbound = calculation_uses_unbounded_bin_value

    def plot(
        self,
        x: np.ndarray[tuple[int], np.dtype[Any]],
        y: np.ndarray[tuple[int], np.dtype[Any]],
        axis: Axes|None = None,
        **kwargs
    ) -> None:
        """
        Plot a hexbin using the colour scheme.

        kwargs will be passed to the `plt.hexbin` function call (or that of the provided axis).
        """

        update_axis: bool = axis is None
        if update_axis:
            axis = plt.gca()

        alpha_calculator = None
        if self.__alpha_calculator is not None:
            alpha_calculator = self.__alpha_calculator(
                typing_cast(float, self.__alpha_calculator_min_return),
                typing_cast(float, self.__alpha_calculator_max_return),
                typing_cast(float, self.__alpha_calculator_min),
                typing_cast(float, self.__alpha_calculator_cap)
            )

        self.__hexes = HexbinRenderer.__modified_hexbin(
            x                 = x,
            y                 = y,
            C                 = np.arange(len(x)),
            reduce_C_function = self.__create_bin_function(
                self.__bin_min,
                self.__bin_max,
                self.__bin_default,
                alpha_calculator,
                self.__alpha_calculator_use_unbound
            ),
            alpha             = self.__alpha_global,
            gridsize          = self.__gridsize,
            cmap              = self.__cmap,
            vmin              = self.__bin_min,
            vmax              = self.__bin_max,
            edgecolor         = self.__edgecolor,
            mincnt            = 0, # Important to always call the colour reduction function
            **kwargs
        )

        if update_axis:
            plt.sci(typing_cast(PolyCollection, self.__hexes))

        if self.__alpha_values is not None:
            typing_cast(PolyCollection, self.__hexes).set_alpha(typing_cast(Sequence[float], self.__alpha_values))

    @staticmethod
    def _create_hexbin_colour_function(statistic: Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]):
        """
        Creates a function around the bin statistic function to work with the HexbinRenderer's
        `plot` method. This is required to allow wrapping of the statistic method for applying the
        configured bin limits.

        This is for internal use and does not need to be manually applied to input functions. This
        is handled internally.
        """

        def ready_hexbin_colour_function(min_value: float|None = None, max_value: float|None = None, default_bin_value: float = -np.inf, alpha_function: Callable[[float, np.ndarray[tuple[int], np.dtype[np.int64]]], float]|None = None, alpha_calculator_use_unbound: bool|None = None):

            @wraps(statistic)
            def calculate_bin_colour_and_alpha(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> tuple[float, float]:
                total_indexes: int = mpi_sum([len(indices)])
                if total_indexes == 0:
                    return default_bin_value, alpha_function(default_bin_value, indices) if alpha_function is not None else 1
                try:
                    result = statistic(indices)
                except Exception as e:
                    if Settings.debug and Settings.verbose:
                        raise e
                    return default_bin_value, alpha_function(default_bin_value, np.array([], dtype = np.int64)) if alpha_function is not None else 1
                if min_value is not None and result < min_value:
                    return min_value, alpha_function(result if alpha_calculator_use_unbound else min_value, indices) if alpha_function is not None else 1
                elif max_value is not None and result > max_value:
                    return max_value, alpha_function(result if alpha_calculator_use_unbound else max_value, indices) if alpha_function is not None else 1
                else:
                    return result, alpha_function(result, indices) if alpha_function is not None else 1

            return calculate_bin_colour_and_alpha

        return ready_hexbin_colour_function

    @staticmethod
    def _create_hexbin_alpha_function(alpha_function: Callable[[float, np.ndarray[tuple[int], np.dtype[np.int64]]], float]):
        """
        Creates a function around the bin alpha function to work with the HexbinRenderer's
        `plot` method. This is required to allow wrapping of the function for applying the
        configured limits.

        This is for internal use and does not need to be manually applied to input functions. This
        is handled internally.
        """

        def ready_hexbin_alpha_function(min_alpha: float, max_alpha: float, alpha_floor: float, alpha_cap: float):

            @wraps(alpha_function)
            def calculate_bin_alpha(bin_value: float, indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
                result = (alpha_function(bin_value, indices) - min_alpha) / (max_alpha - min_alpha)
                if result < alpha_floor:
                    return 0
                elif result > alpha_cap:
                    return alpha_cap
                else:
                    return result

            return calculate_bin_alpha

        return ready_hexbin_alpha_function

    # Built-in bin statistic functions

    @staticmethod
    def bin_statistic_count(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
        """
        Assign hexbin value to the number of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(I,), numpy.int64]` indices:
                The indexes into the x and y data arrays that identify the points that fall into
                the bin.

        Returns `float`:
            The number of elements within the bin.
        """
        return float(mpi_sum(len(indices)))

    @staticmethod
    def bin_statistic_log10_count(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
        """
        Assign hexbin value to log_10 of the number of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(I,), numpy.int64]` indices:
                The indexes into the x and y data arrays that identify the points that fall into
                the bin.

        Returns `float`:
            The number of elements within the bin.
        """
        return np.log10(HexbinRenderer.bin_statistic_count(indices = indices))

    @staticmethod
    def gather_bin_values(data: np.ndarray[tuple[int], np.dtype[T]], indices: np.ndarray[tuple[int], np.dtype[np.int64]]) -> np.ndarray[tuple[int], np.dtype[T]]:
        """
        Helper function for gathering bin data separated across multiple MPI ranks.
        This is in effect an 'allgather' operation.
        """
        return mpi_gather_array(data[indices], allgather = True)

    @staticmethod
    def create_bin_statistic_sum(data: np.ndarray[tuple[int], np.dtype[float]]) -> Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Assign hexbin value to the number of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(N,), float]` data:
                Data elements - the same shape as the x and y data arrays.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            A bin statistic for the number of elements within the bin.
        """
        def bin_statistic_sum(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Assign hexbin value to the number of elements that fall within each bin.

            Parameters:
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The number of elements within the bin.
            """
            return float(mpi_sum(data[indices]))
        return bin_statistic_sum

    @staticmethod
    def create_bin_statistic_log10_sum(data: np.ndarray[tuple[int], np.dtype[float]], initial_offset: float = 0.0, final_offset: float = 1.0) -> Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Assign hexbin value to log_10 of the number of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(N,), float]` data:
                Data elements - the same shape as the x and y data arrays.
            (optional) `float` initial_offset:
                Value to add to each data value BEFORE summation. This is necessary when the data
                values can be 0!
                Default is 0.
            (optional) `float` final_offset:
                A value to add to the final result - useful for unit conversions.
                NOTE: this value is not passed through the log_10 function. When applying unit
                conversions, most units will require a value of `-numpy.log10(value_of_unit)`!
                Default is 1.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            A bin statistic for log_10 of the number of elements within the bin.
        """
        def bin_statistic_log10_sum(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Assign hexbin value to log_10 of the number of elements that fall within each bin.

            Parameters:
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The number log_10 of elements within the bin.
            """
            return float(np.log10(mpi_sum(data[indices] + initial_offset))) + final_offset
        return bin_statistic_log10_sum

    @staticmethod
    def create_bin_statistic_mean(data: np.ndarray[tuple[int], np.dtype[float]], weights: np.ndarray[tuple[int], np.dtype[float]]|None = None) -> Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Assign hexbin value to the mean of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(N,), float]` data:
                Data elements - the same shape as the x and y data arrays.
            (optional) `numpy.ndarray[(N,), float]|None` weights:
                One weight per data element.
                Default is `None`.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            A bin statistic for the mean of elements within the bin.
        """
        def bin_statistic_weighted_mean(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Assign hexbin value to the mean of elements that fall within each bin.

            Parameters:
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The mean of elements within the bin.
            """
            return float(mpi_mean(data[indices], weights = weights[indices] if weights is not None else None))
        return bin_statistic_weighted_mean

    @staticmethod
    def create_bin_statistic_median(data: np.ndarray[tuple[int], np.dtype[float]]) -> Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Assign hexbin value to the median of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(N,), float]` data:
                Data elements - the same shape as the x and y data arrays.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            A bin statistic for the median of elements within the bin.
        """
        def bin_statistic_median(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
        Assign hexbin value to the median of elements that fall within each bin.

            Parameters:
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The median of elements within the bin.
            """

            return float(np.median(HexbinRenderer.gather_bin_values(data, indices)))
        return bin_statistic_median

    @staticmethod
    def create_bin_statistic_percentile(data: np.ndarray[tuple[int], np.dtype[float]], percentile: float) -> Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Assign hexbin value to the percentile value from elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(N,), float]` data:
                Data elements - the same shape as the x and y data arrays.
            `float` percentile:
                The percentile at which compute the value.
                [0 -> 100]

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            A bin statistic for the percentile value of elements within the bin.
        """
        def bin_statistic_percentile(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Assign hexbin value to the percentile value from elements that fall within each bin.

            Parameters:
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The percentile value of elements within the bin.
            """

            return float(np.percentile(HexbinRenderer.gather_bin_values(data, indices), percentile))
        return bin_statistic_percentile
    
    @staticmethod
    def create_bin_statistic_log10_mean(data: np.ndarray[tuple[int], np.dtype[float]], weights: np.ndarray[tuple[int], np.dtype[float]]|None = None, initial_offset: float = 0.0, final_offset: float = 1.0) -> Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Assign hexbin value to the mean of elements that fall within each bin.

        Parameters:
            `numpy.ndarray[(N,), float]` data:
                Data elements - the same shape as the x and y data arrays.
            (optional) `numpy.ndarray[(N,), float]|None` weights:
                One weight per data element.
                Default is `None`.
            (optional) `float` initial_offset:
                Value to add to each data value BEFORE summation. This is necessary when the data
                values can be 0!
                Default is 0.
            (optional) `float` final_offset:
                A value to add to the final result - useful for unit conversions.
                NOTE: this value is not passed through the log_10 function. When applying unit
                conversions, most units will require a value of `-numpy.log10(value_of_unit)`!
                Default is 1.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            A bin statistic for log_10 of the mean of elements within the bin.
        """
        def bin_statistic_log10_weighted_mean(indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Assign hexbin value to the mean of elements that fall within each bin.

            Parameters:
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                log_10 of the mean of elements within the bin.
            """
            return float(np.log10(mpi_mean(data[indices] + initial_offset, weights = weights[indices] if weights is not None else None))) + final_offset
        return bin_statistic_log10_weighted_mean

    # Built-in bin alpha functions

    @staticmethod
    def bin_alpha_value(bin_value: float, indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
        """
        Use the value of the bin to set the alpha value of the hex.

        Parameters:
            `float` bin_value:
                The calculated value for the bin.
            `numpy.ndarray[(I,), numpy.int64]` indices:
                The indexes into the x and y data arrays that identify the points that fall into
                the bin.

        Returns `float`:
            The value of the bin.
        """
        return bin_value

    @staticmethod
    def bin_alpha_reciprocal_value(bin_value: float, indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
        """
        Use the reciprocal of the value of the bin to set the alpha value of the hex.

        Parameters:
            `float` bin_value:
                The calculated value for the bin.
            `numpy.ndarray[(I,), numpy.int64]` indices:
                The indexes into the x and y data arrays that identify the points that fall into
                the bin.

        Returns `float`:
            The reciprocal (1/x) of the value of the bin.
            If `len(indices)` is 0, numpy.Infinity is returned.
        """
        return (1 / bin_value) if bin_value != 0 else np.Infinity

    @staticmethod
    def create_bin_alpha_statistic(statistic: Callable[[np.ndarray[tuple[int], np.dtype[np.int64]]], float]) -> Callable[[float, np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Use an existing statistic function to set the alpha value of the hex.

        Parameters:
            `Callable[[np.ndarray[(I,), numpy.int64]], float]` statistic:
                A bin statistic function used to calculate a value from the indexes giving which
                elements fall within a given bin.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            The wrapped statistic function.
        """
        def bin_statistic_sum(bin_value: float, indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Use an existing statistic function to set the alpha value of the hex.

            Parameters:
                `float` bin_value:
                    The calculated value for the bin.
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The statistic for the bin.
            """
            return statistic(indices)
        return bin_statistic_sum

    @staticmethod
    def create_bin_alpha_value_converter(conversion_function: Callable[[float], float]) -> Callable[[float, np.ndarray[tuple[int], np.dtype[np.int64]]], float]:
        """
        Use a function to set the alpha value of the hex using the hex's value.

        Parameters:
            `Callable[[float], float]` conversion_function:
                Function used to convert a bin's calculated value into an alpha value.

        Returns `Callable[[numpy.ndarray[(I,), numpy.int64]], float]`:
            The wrapped conversion function.
        """
        def bin_statistic_sum(bin_value: float, indices: np.ndarray[tuple[int], np.dtype[np.int64]], /) -> float:
            """
            Use a function to set the alpha value of the hex using the hex's value.

            Parameters:
                `float` bin_value:
                    The calculated value for the bin.
                `numpy.ndarray[(I,), numpy.int64]` indices:
                    The indexes into the x and y data arrays that identify the points that fall
                    into the bin.

            Returns `float`:
                The alpha value for the bin.
            """
            return conversion_function(bin_value)
        return bin_statistic_sum



    @staticmethod
    @_preprocess_data(replace_names=["x", "y", "C"], label_namer="y")
    @dedent_interpd
    def __modified_hexbin(self, x, y, C=None, gridsize=100, bins=None,
               xscale='linear', yscale='linear', extent=None,
               cmap=None, norm=None, vmin=None, vmax=None,
               alpha=None, linewidths=None, edgecolors='face',
               reduce_C_function=np.mean, mincnt=None, marginals=False,
               **kwargs) -> PolyCollection:
        """
        Lifted from matplotlib.axes._axes as there is no modular version.
        Edits are made to facilitate the on-the-fly calculation of alpha values.
        MPI support has also been added to allow use with large datasets.
        Source code is only edited where necessary and is otherwise left as-is.

        The original docstring is as follows:

        Make a 2D hexagonal binning plot of points *x*, *y*.

        If *C* is *None*, the value of the hexagon is determined by the number
        of points in the hexagon. Otherwise, *C* specifies values at the
        coordinate (x[i], y[i]). For each hexagon, these values are reduced
        using *reduce_C_function*.

        Parameters
        ----------
        x, y : array-like
            The data positions. *x* and *y* must be of the same length.

        C : array-like, optional
            If given, these values are accumulated in the bins. Otherwise,
            every point has a value of 1. Must be of the same length as *x*
            and *y*.

        gridsize : int or (int, int), default: 100
            If a single int, the number of hexagons in the *x*-direction.
            The number of hexagons in the *y*-direction is chosen such that
            the hexagons are approximately regular.

            Alternatively, if a tuple (*nx*, *ny*), the number of hexagons
            in the *x*-direction and the *y*-direction. In the
            *y*-direction, counting is done along vertically aligned
            hexagons, not along the zig-zag chains of hexagons; see the
            following illustration.

            .. plot::

               import numpy
               import matplotlib.pyplot as plt

               np.random.seed(19680801)
               n= 300
               x = np.random.standard_normal(n)
               y = np.random.standard_normal(n)

               fig, ax = plt.subplots(figsize=(4, 4))
               h = ax.hexbin(x, y, gridsize=(5, 3))
               hx, hy = h.get_offsets().T
               ax.plot(hx[24::3], hy[24::3], 'ro-')
               ax.plot(hx[-3:], hy[-3:], 'ro-')
               ax.set_title('gridsize=(5, 3)')
               ax.axis('off')

            To get approximately regular hexagons, choose
            :math:`n_x = \\sqrt{3}\\,n_y`.

        bins : 'log' or int or sequence, default: None
            Discretization of the hexagon values.

            - If *None*, no binning is applied; the color of each hexagon
              directly corresponds to its count value.
            - If 'log', use a logarithmic scale for the colormap.
              Internally, :math:`log_{10}(i+1)` is used to determine the
              hexagon color. This is equivalent to ``norm=LogNorm()``.
            - If an integer, divide the counts in the specified number
              of bins, and color the hexagons accordingly.
            - If a sequence of values, the values of the lower bound of
              the bins to be used.

        xscale : {'linear', 'log'}, default: 'linear'
            Use a linear or log10 scale on the horizontal axis.

        yscale : {'linear', 'log'}, default: 'linear'
            Use a linear or log10 scale on the vertical axis.

        mincnt : int >= 0, default: *None*
            If not *None*, only display cells with at least *mincnt*
            number of points in the cell.

        marginals : bool, default: *False*
            If marginals is *True*, plot the marginal density as
            colormapped rectangles along the bottom of the x-axis and
            left of the y-axis.

        extent : 4-tuple of float, default: *None*
            The limits of the bins (xmin, xmax, ymin, ymax).
            The default assigns the limits based on
            *gridsize*, *x*, *y*, *xscale* and *yscale*.

            If *xscale* or *yscale* is set to 'log', the limits are
            expected to be the exponent for a power of 10. E.g. for
            x-limits of 1 and 50 in 'linear' scale and y-limits
            of 10 and 1000 in 'log' scale, enter (1, 50, 1, 3).

        Returns
        -------
        `~matplotlib.collections.PolyCollection`
            A `.PolyCollection` defining the hexagonal bins.

            - `.PolyCollection.get_offsets` contains a Mx2 array containing
              the x, y positions of the M hexagon centers.
            - `.PolyCollection.get_array` contains the values of the M
              hexagons.

            If *marginals* is *True*, horizontal
            bar and vertical bar (both PolyCollections) will be attached
            to the return collection as attributes *hbar* and *vbar*.

        Other Parameters
        ----------------
        %(cmap_doc)s

        %(norm_doc)s

        %(vmin_vmax_doc)s

        alpha : float between 0 and 1, optional
            The alpha blending value, between 0 (transparent) and 1 (opaque).

        linewidths : float, default: *None*
            If *None*, defaults to :rc:`patch.linewidth`.

        edgecolors : {'face', 'none', *None*} or color, default: 'face'
            The color of the hexagon edges. Possible values are:

            - 'face': Draw the edges in the same color as the fill color.
            - 'none': No edges are drawn. This can sometimes lead to unsightly
              unpainted pixels between the hexagons.
            - *None*: Draw outlines in the default color.
            - An explicit color.

        reduce_C_function : callable, default: `numpy.mean`
            The function to aggregate *C* within the bins. It is ignored if
            *C* is not given. This must have the signature::

                def reduce_C_function(C: array) -> float

            Commonly used functions are:

            - `numpy.mean`: average of the points
            - `numpy.sum`: integral of the point values
            - `numpy.amax`: value taken from the largest point

            By default will only reduce cells with at least 1 point because some
            reduction functions (such as `numpy.amax`) will error/warn with empty
            input. Changing *mincnt* will adjust the cutoff, and if set to 0 will
            pass empty input to the reduction function.

        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER

        **kwargs : `~matplotlib.collections.PolyCollection` properties
            All other keyword arguments are passed on to `.PolyCollection`:

            %(PolyCollection:kwdoc)s

        See Also
        --------
        hist2d : 2D histogram rectangular bins
        """
        self._process_unit_info([("x", x), ("y", y)], kwargs, convert=False)

        x, y, C = cbook.delete_masked_points(x, y, C)

        # Set the size of the hexagon grid
        if np.iterable(gridsize):
            nx, ny = gridsize
        else:
            nx = gridsize
            ny = int(nx / math.sqrt(3))
        # Count the number of data in each hexagon
        x = np.asarray(x, float)
        y = np.asarray(y, float)

        # Will be log()'d if necessary, and then rescaled.
        tx = x
        ty = y

        if xscale == 'log':
            if np.any(x <= 0.0):
                raise ValueError(
                    "x contains non-positive values, so cannot be log-scaled")
            tx = np.log10(tx)
        if yscale == 'log':
            if np.any(y <= 0.0):
                raise ValueError(
                    "y contains non-positive values, so cannot be log-scaled")
            ty = np.log10(ty)
        if extent is not None:
            xmin, xmax, ymin, ymax = extent
        else:
            xmin, xmax = (tx.min(), tx.max()) if len(x) else (0, 1)
            ymin, ymax = (ty.min(), ty.max()) if len(y) else (0, 1)

            # to avoid issues with singular data, expand the min/max pairs
            xmin, xmax = mtransforms.nonsingular(xmin, xmax, expander=0.1)
            ymin, ymax = mtransforms.nonsingular(ymin, ymax, expander=0.1)

        nx1 = nx + 1
        ny1 = ny + 1
        nx2 = nx
        ny2 = ny
        n = nx1 * ny1 + nx2 * ny2

        # In the x-direction, the hexagons exactly cover the region from
        # xmin to xmax. Need some padding to avoid roundoff errors.
        padding = 1.e-9 * (xmax - xmin)
        xmin -= padding
        xmax += padding
        sx = (xmax - xmin) / nx
        sy = (ymax - ymin) / ny
        # Positions in hexagon index coordinates.
        ix = (tx - xmin) / sx
        iy = (ty - ymin) / sy
        ix1 = np.round(ix).astype(int)
        iy1 = np.round(iy).astype(int)
        ix2 = np.floor(ix).astype(int)
        iy2 = np.floor(iy).astype(int)
        # flat indices, plus one so that out-of-range points go to position 0.
        i1 = np.where((0 <= ix1) & (ix1 < nx1) & (0 <= iy1) & (iy1 < ny1),
                      ix1 * ny1 + iy1 + 1, 0)
        i2 = np.where((0 <= ix2) & (ix2 < nx2) & (0 <= iy2) & (iy2 < ny2),
                      ix2 * ny2 + iy2 + 1, 0)

        d1 = (ix - ix1) ** 2 + 3.0 * (iy - iy1) ** 2
        d2 = (ix - ix2 - 0.5) ** 2 + 3.0 * (iy - iy2 - 0.5) ** 2
        bdist = (d1 < d2)

        if C is None:  # [1:] drops out-of-range points.
            counts1 = np.bincount(i1[bdist], minlength=1 + nx1 * ny1)[1:]
            counts2 = np.bincount(i2[~bdist], minlength=1 + nx2 * ny2)[1:]
            accum = np.concatenate([counts1, counts2]).astype(float)
            if mincnt is not None:
                accum[accum < mincnt] = np.nan
            C = np.ones(len(x))
        else:
            # store the C values in a list per hexagon index
            Cs_at_i1 = [[] for _ in range(1 + nx1 * ny1)]
            Cs_at_i2 = [[] for _ in range(1 + nx2 * ny2)]
            for i in range(len(x)):
                if bdist[i]:
                    Cs_at_i1[i1[i]].append(C[i])
                else:
                    Cs_at_i2[i2[i]].append(C[i])
            if mincnt is None:
                mincnt = 1
            accum = np.array(
                [reduce_C_function(acc) if len(acc) >= mincnt else np.nan
                 for Cs_at_i in [Cs_at_i1, Cs_at_i2]
                 for acc in Cs_at_i[1:]],  # [1:] drops out-of-range points.
                float)

        good_idxs = ~np.isnan(accum)

        offsets = np.zeros((n, 2), float)
        offsets[:nx1 * ny1, 0] = np.repeat(np.arange(nx1), ny1)
        offsets[:nx1 * ny1, 1] = np.tile(np.arange(ny1), nx1)
        offsets[nx1 * ny1:, 0] = np.repeat(np.arange(nx2) + 0.5, ny2)
        offsets[nx1 * ny1:, 1] = np.tile(np.arange(ny2), nx2) + 0.5
        offsets[:, 0] *= sx
        offsets[:, 1] *= sy
        offsets[:, 0] += xmin
        offsets[:, 1] += ymin
        # remove accumulation bins with no data
        offsets = offsets[good_idxs, :]
        accum = accum[good_idxs]

        polygon = [sx, sy / 3] * np.array(
            [[.5, -.5], [.5, .5], [0., 1.], [-.5, .5], [-.5, -.5], [0., -1.]])

        if linewidths is None:
            linewidths = [mpl.rcParams['patch.linewidth']]

        if xscale == 'log' or yscale == 'log':
            polygons = np.expand_dims(polygon, 0) + np.expand_dims(offsets, 1)
            if xscale == 'log':
                polygons[:, :, 0] = 10.0 ** polygons[:, :, 0]
                xmin = 10.0 ** xmin
                xmax = 10.0 ** xmax
                self.set_xscale(xscale)
            if yscale == 'log':
                polygons[:, :, 1] = 10.0 ** polygons[:, :, 1]
                ymin = 10.0 ** ymin
                ymax = 10.0 ** ymax
                self.set_yscale(yscale)
            collection = mcoll.PolyCollection(
                polygons,
                edgecolors=edgecolors,
                linewidths=linewidths,
                )
        else:
            collection = mcoll.PolyCollection(
                [polygon],
                edgecolors=edgecolors,
                linewidths=linewidths,
                offsets=offsets,
                offset_transform=mtransforms.AffineDeltaTransform(
                    self.transData),
            )

        # Set normalizer if bins is 'log'
        if cbook._str_equal(bins, 'log'):
            if norm is not None:
                _api.warn_external("Only one of 'bins' and 'norm' arguments "
                                   f"can be supplied, ignoring {bins=}")
            else:
                norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
                vmin = vmax = None
            bins = None

        # autoscale the norm with current accum values if it hasn't been set
        if norm is not None:
            if norm.vmin is None and norm.vmax is None:
                norm.autoscale(accum)

        if bins is not None:
            if not np.iterable(bins):
                minimum, maximum = min(accum), max(accum)
                bins -= 1  # one less edge than bins
                bins = minimum + (maximum - minimum) * np.arange(bins) / bins
            bins = np.sort(bins)
            accum = bins.searchsorted(accum)

        collection.set_array(accum)
        collection.set_cmap(cmap)
        collection.set_norm(norm)
        collection.set_alpha(alpha)
        collection._internal_update(kwargs)
        collection._scale_norm(norm, vmin, vmax)

        corners = ((xmin, ymin), (xmax, ymax))
        self.update_datalim(corners)
        self._request_autoscale_view(tight=True)

        # add the collection last
        self.add_collection(collection, autolim=False)
        if not marginals:
            return collection

        # Process marginals
        bars = []
        for zname, z, zmin, zmax, zscale, nbins in [
                ("x", x, xmin, xmax, xscale, nx),
                ("y", y, ymin, ymax, yscale, 2 * ny),
        ]:

            if zscale == "log":
                bin_edges = np.geomspace(zmin, zmax, nbins + 1)
            else:
                bin_edges = np.linspace(zmin, zmax, nbins + 1)

            verts = np.empty((nbins, 4, 2))
            verts[:, 0, 0] = verts[:, 1, 0] = bin_edges[:-1]
            verts[:, 2, 0] = verts[:, 3, 0] = bin_edges[1:]
            verts[:, 0, 1] = verts[:, 3, 1] = .00
            verts[:, 1, 1] = verts[:, 2, 1] = .05
            if zname == "y":
                verts = verts[:, :, ::-1]  # Swap x and y.

            # Sort z-values into bins defined by bin_edges.
            bin_idxs = np.searchsorted(bin_edges, z) - 1
            values = np.empty(nbins)
            for i in range(nbins):
                # Get C-values for each bin, and compute bin value with
                # reduce_C_function.
                ci = C[bin_idxs == i]
                values[i] = reduce_C_function(ci) if len(ci) > 0 else np.nan

            mask = ~np.isnan(values)
            verts = verts[mask]
            values = values[mask]

            trans = getattr(self, f"get_{zname}axis_transform")(which="grid")
            bar = mcoll.PolyCollection(
                verts, transform=trans, edgecolors="face")
            bar.set_array(values)
            bar.set_cmap(cmap)
            bar.set_norm(norm)
            bar.set_alpha(alpha)
            bar._internal_update(kwargs)
            bars.append(self.add_collection(bar, autolim=False))

        collection.hbar, collection.vbar = bars

        def on_changed(collection):
            collection.hbar.set_cmap(collection.get_cmap())
            collection.hbar.set_cmap(collection.get_cmap())
            collection.vbar.set_clim(collection.get_clim())
            collection.vbar.set_clim(collection.get_clim())

        collection.callbacks.connect('changed', on_changed)

        return collection
