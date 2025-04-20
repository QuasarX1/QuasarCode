from typing import Any, Literal, Sequence, TypeVar
from abc import abstractmethod

from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar
from matplotlib.colorizer import ColorizingArtist
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from matplotlib.pylab import ArrayLike
from matplotlib.typing import ColorType, MarkerType
import numpy as np
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.container import ErrorbarContainer
from matplotlib.lines import Line2D

from ..Data._Rect import Rect
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable

T = TypeVar("T")

class CachedPlotElement[T](CacheableStruct):
    _result = AutoProperty[T]()
    def __init__(self, *cacheable_attributes: str, **kwargs):
        super().__init__(
            cacheable_attributes = cacheable_attributes,#list(cacheable_attributes) + ["_result"],
            **kwargs
        )
    @property
    def result(self) -> T|None:
        return self._result
    @abstractmethod
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any) -> None:
        """
        Render the element on the given figure and axis.
        
        Parameters:
            matplotlib.figure.Figure figure:
                The figure to render on.
            matplotlib.axes.Axes axis:
                The axis to render on.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class CachedPlotLine(CachedPlotElement[Line2D]):
    x = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    y = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    label = AutoProperty[str]()
    colour = AutoProperty[ColorType]()
    linestyle = AutoProperty[str]()
    linewidth = AutoProperty[float]()
    alpha = AutoProperty_NonNullable[float](default_value = 1.0)
    def __init__(self, **kwargs):
        super().__init__("x", "y", "label", "colour", "linestyle", "linewidth", "alpha", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any) -> None:
        self._result = axis.plot(self.x, self.y, label = self.label, colour = self.colour, linestyle = self.linestyle, linewidth = self.linewidth, alpha = self.alpha)[0]
    @staticmethod
    def from_line(line: Line2D) -> "CachedPlotLine":
        coords: np.ndarray[tuple[int, int], np.dtype[np.floating]] = line.get_xydata()
        return CachedPlotLine(
            x = coords[:, 0],
            y = coords[:, 1],
            label = line.get_label(),
            colour = line.get_color(),
            linestyle = line.get_linestyle(),
            linewidth = line.get_linewidth(),
            alpha = line.get_alpha(),
            _result = line
        )

class CachedPlotScatter(CachedPlotElement[PathCollection]):
    x = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    y = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    label = AutoProperty[str]()
    colour = AutoProperty[ColorType|Sequence[ColorType]]()
    colourmap = AutoProperty[str|Colormap]()
    marker = AutoProperty[MarkerType]()
    size = AutoProperty[float|ArrayLike]()
    alpha = AutoProperty[float|ArrayLike]()
    def __init__(self, **kwargs):
        super().__init__("x", "y", "label", "colour", "colourmap", "marker", "size", "alpha", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any):
        self._result = axis.scatter(self.x, self.y, c = self.colour, cmap = self.colourmap, marker = self.marker, s = self.size, alpha = self.alpha, label = self.label, **kwargs)
    @staticmethod
    def from_points(points: PathCollection) -> "CachedPlotScatter":
        coords: np.ndarray[tuple[int, int], np.dtype[np.floating]] = points.get_offsets()
        return CachedPlotScatter(
            x = coords[:, 0],
            y = coords[:, 1],
            label = points.get_label(),
            colour = points.get_facecolor(),
            colourmap = points.get_cmap(),
            marker = points.get_paths()[0],
            size = points.get_sizes(),
            alpha = points.get_alpha(),
            _result = points
        )

class CachedPlotErrorbar(CachedPlotElement[ErrorbarContainer]):
    x = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    y = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    xerr = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    yerr = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    colourmap = AutoProperty[str|Colormap]()
    def __init__(self, **kwargs):
        super().__init__("x", "y", "xerr", "yerr", "colourmap", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any):
        self._result = axis.errorbar(self.x, self.y, self.yerr, self.xerr, cmap = self.colourmap)

class CachedPlotHexbin(CachedPlotElement[PolyCollection]):
    extent = AutoProperty_NonNullable[Rect]()
    gridsize = AutoProperty_NonNullable[int|tuple[int, int]]()
    polygon_offsets = AutoProperty_NonNullable[np.ndarray[tuple[int, int], np.dtype[np.floating]]]()
    bin_values = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    min_value = AutoProperty[float]()
    max_value = AutoProperty[float]()
    colourmap = AutoProperty[str|Colormap]()
    edgecolour = AutoProperty_NonNullable[ColorType|Literal["face", "none"]](default_value = "face")
    bin_alphas = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    def __init__(self, **kwargs):
        super().__init__("extent", "gridsize", "polygon_offsets", "bin_values", "min_value", "max_value", "colourmap", "edgecolour", "bin_alphas", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any):
        self._result = axis.hexbin(
            x = self.polygon_offsets[:, 0],
            y = self.polygon_offsets[:, 1],
            C = self.bin_values,
            gridsize = self.gridsize,
            cmap = self.colourmap,
            vmin = self.min_value,
            vmax = self.max_value,
            edgecolor = self.edgecolour,
            extent = self.extent.extent
        )
        self._result.set_alpha(self.bin_alphas) # type: ignore[arg-type]
    @staticmethod
    def from_hexes(hexes: PolyCollection, extent: Rect, gridsize: int, min_value: float|None = None, max_value: float|None = None, colourmap: str|None = None) -> "CachedPlotHexbin":
        return CachedPlotHexbin(
            extent = extent,
            gridsize = gridsize,
            polygon_offsets = hexes.get_offsets(),
            bin_values = hexes.get_array(),
            min_value = min_value,
            max_value = max_value,
            edgecolour = hexes.get_edgecolor(),
            colourmap = colourmap,
            bin_alphas = hexes.get_alpha()
        )

class CachedPlotColourbar(CachedPlotElement[Colorbar]):
    target_element = AutoProperty_NonNullable[str]()
    label =  AutoProperty[str]()
    location =  AutoProperty[Literal["left", "right", "top", "bottom"]]()
    extend = AutoProperty[Literal["neither", "both", "min", "max"]]()
    bin_alphas = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    def __init__(self, **kwargs):
        super().__init__("target_element", "label", "location", "extend", **kwargs)
    def render(self, figure: Figure, axis: Axes, target: ScalarMappable|ColorizingArtist, *args: Any, **kwargs: Any) -> None:
        """
        Render the element on the given figure and axis, using the target element.
        
        Parameters:
            matplotlib.figure.Figure figure:
                The figure to render on.
            matplotlib.axes.Axes axis:
                The axis to render on.
            ScalarMappable|ColorizingArtist target:
                The target element for the colourbar.
        """
        self._result = figure.colorbar(
            target,
            ax = axis,
            location = self.location,
            label = self.label,
            extend = self.extend
        )
