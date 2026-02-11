from typing import TYPE_CHECKING, Any, Literal, Sequence, TypeVar, Generic
from abc import abstractmethod

from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar
from matplotlib.colorizer import ColorizingArtist
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
if TYPE_CHECKING:
    from matplotlib.pylab import ArrayLike
from matplotlib.typing import ColorType, MarkerType
import numpy as np
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.container import ErrorbarContainer
from matplotlib.lines import Line2D
from matplotlib.contour import QuadContourSet
from matplotlib.image import AxesImage
from matplotlib.text import Text
from matplotlib.patches import Wedge

from ..Data._Rect import Rect
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable
from ..Tools._CacheableFunction import CacheableFunction
from ._CachedPlotFontInfo import CachedPlotFontInfo

T = TypeVar("T")

class CachedPlotElement(CacheableStruct, Generic[T]):
    _result = AutoProperty[T](allow_uninitialised = True)
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
    label = AutoProperty[str](allow_uninitialised = True)
    colour = AutoProperty[ColorType](allow_uninitialised = True)
    linestyle = AutoProperty[str](allow_uninitialised = True)
    linewidth = AutoProperty[float](allow_uninitialised = True)
    alpha = AutoProperty_NonNullable[float](default_value = 1.0)
    def __init__(self, **kwargs):
        super().__init__("x", "y", "label", "colour", "linestyle", "linewidth", "alpha", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any) -> None:
        self._result = axis.plot(
            self.x,
            self.y,
            label = self.label,
            color = self.colour,
            linestyle = self.linestyle,
            linewidth = self.linewidth,
            alpha = self.alpha,
            **kwargs
        )[0]
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
    label = AutoProperty[str](allow_uninitialised = True)
    colour = AutoProperty[ColorType|Sequence[ColorType]](allow_uninitialised = True)
    colourmap = AutoProperty[str|Colormap](allow_uninitialised = True)
    marker = AutoProperty[MarkerType](allow_uninitialised = True)
    size = AutoProperty["float|ArrayLike"](allow_uninitialised = True)
    alpha = AutoProperty["float|ArrayLike"](allow_uninitialised = True)
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
    xerr = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]](allow_uninitialised = True)
    yerr = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]](allow_uninitialised = True)
    label = AutoProperty[str](allow_uninitialised = True)
    line_colour = AutoProperty[ColorType|Sequence[ColorType]](allow_uninitialised = True)
    marker_colour = AutoProperty[ColorType|Sequence[ColorType]](allow_uninitialised = True)
    error_colour = AutoProperty[ColorType|Sequence[ColorType]](allow_uninitialised = True)
    error_line_width = AutoProperty[float](allow_uninitialised = True)
    colourmap = AutoProperty[str|Colormap](allow_uninitialised = True)
    marker = AutoProperty[MarkerType](allow_uninitialised = True, default_value = "")
    size = AutoProperty["float|ArrayLike"](allow_uninitialised = True)
    alpha = AutoProperty["float|ArrayLike"](allow_uninitialised = True)
    def __init__(self, **kwargs):
        super().__init__("x", "y", "xerr", "yerr", "colourmap", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any):
        self._result = axis.errorbar(
            x = self.x,
            y = self.y,
            yerr = self.yerr,
            xerr = self.xerr,
            label = self.label,
            ecolor = self.error_colour,
            elinewidth = self.error_line_width,
            cmap = self.colourmap,
            marker = self.marker,
            markersize = self.size,
            alpha = self.alpha,
            color = self.line_colour,
            **kwargs
        )
    @staticmethod
    def from_errorbar(bars: ErrorbarContainer) -> "CachedPlotErrorbar":
        coords: np.ndarray[tuple[int, int], np.dtype[np.floating]] = bars.get_offsets()
        return CachedPlotErrorbar(
            x = coords[:, 0],
            y = coords[:, 1],
            label = bars.get_label(),
            colour = bars.get_facecolor(),
            colourmap = bars.get_cmap(),
            marker = bars.get_paths()[0],
            size = bars.get_sizes(),
            alpha = bars.get_alpha(),
            _result = bars
        )

class CachedPlotHexbin(CachedPlotElement[PolyCollection]):
    extent = AutoProperty_NonNullable[Rect]()
    gridsize = AutoProperty_NonNullable[int|tuple[int, int]]()
    polygon_offsets = AutoProperty_NonNullable[np.ndarray[tuple[int, int], np.dtype[np.floating]]]()
    bin_values = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    min_value = AutoProperty[float](allow_uninitialised = True)
    max_value = AutoProperty[float](allow_uninitialised = True)
    colourmap = AutoProperty[str|Colormap](allow_uninitialised = True)
    edgecolour = AutoProperty_NonNullable[ColorType|Literal["face", "none"]](default_value = "face")
    bin_alphas = AutoProperty[np.ndarray[tuple[int], np.dtype[np.floating]]](allow_uninitialised = True)
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
            extent = self.extent.extent,
            **kwargs
        )
        self._result.set_alpha(self.bin_alphas) # type: ignore[arg-type]
    @staticmethod
    def from_hexes(hexes: PolyCollection, extent: Rect, gridsize: int|tuple[int, int], min_value: float|None = None, max_value: float|None = None, edgecolours_match_faces: bool = False) -> "CachedPlotHexbin":
        n_hexes = hexes.get_array().shape[0]
        edgecolour = hexes.get_edgecolor()
        if edgecolours_match_faces:
            edgecolour = "face"
        elif isinstance(edgecolour, np.ndarray) and edgecolour.shape[0] == 0 and n_hexes > 0:
            edgecolour = "none"
        return CachedPlotHexbin(
            extent = extent,
            gridsize = gridsize,
            polygon_offsets = hexes.get_offsets(),
            bin_values = hexes.get_array(),
            min_value = min_value,
            max_value = max_value,
            edgecolour = edgecolour,
            colourmap = hexes.get_cmap(),
            bin_alphas = hexes.get_alpha(),
            _result = hexes
        )

class CachedPlotColourbar(CachedPlotElement[Colorbar]):
    target_element  = AutoProperty_NonNullable[str]()
    target_plot     = AutoProperty[str](allow_uninitialised = True)
    label           = AutoProperty[str](allow_uninitialised = True)
    add_to_axis     = AutoProperty_NonNullable[bool](default_value = True)
    location        = AutoProperty[Literal["left", "right", "top", "bottom"]|None](default_value = "right", allow_uninitialised = True)
    orientation     = AutoProperty[Literal["horizontal", "vertical", "top", "bottom"]](default_value = "vertical")
    extend          = AutoProperty[Literal["neither", "both", "min", "max"]](default_value = "neither")
    default_font    = AutoProperty_NonNullable[CachedPlotFontInfo]()
    label_font      = AutoProperty_NonNullable[CachedPlotFontInfo]()
    tick_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    def __init__(self, **kwargs):
        super().__init__("target_element", "target_plot", "label", "add_to_axis", "location", "orientation", "extend", "label_font", "tick_label_font", **kwargs)
        self.label_font = CachedPlotFontInfo()
    def render(self, figure: Figure, axis: Axes, target: ScalarMappable|ColorizingArtist, default_font: CachedPlotFontInfo, *args: Any, **kwargs: Any) -> None:
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
            ax = axis if self.add_to_axis else None,
            cax = axis if not self.add_to_axis else None,
            location = self.location if self.add_to_axis else None,
            label = self.label,
            extend = self.extend,
            orientation = self.orientation if not self.add_to_axis else None,
            **kwargs
        )
        self._result.ax.xaxis.label.set_fontproperties(self.label_font.with_default(self.default_font).with_default(default_font).fontproperties)
        self._result.ax.yaxis.label.set_fontproperties(self.label_font.with_default(self.default_font).with_default(default_font).fontproperties)
        tick_label_font = self.tick_label_font.with_default(self.default_font).with_default(default_font)
        self._result.ax.tick_params(
            labelsize       = tick_label_font.size,
            labelcolor      = tick_label_font.color,
            labelfontfamily = tick_label_font.family,
        )

class CachedPlotContour(CachedPlotElement[QuadContourSet]):
    x = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    y = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    z = AutoProperty_NonNullable[np.ndarray[tuple[int, int], np.dtype[np.floating]]]()
    levels = AutoProperty_NonNullable[tuple[float]]()
    linewidths = AutoProperty["ArrayLike"](allow_uninitialised = True)
    linestyles = AutoProperty[tuple[Literal["solid", "dashed", "dashdot", "dotted"]]](allow_uninitialised = True)
    alpha_values = AutoProperty[tuple["float|ArrayLike"]](allow_uninitialised = True)
    colours = AutoProperty[tuple[ColorType]](allow_uninitialised = True)
    def __init__(self, **kwargs):
        super().__init__("x", "y", "z", "levels", "linewidths", "linestyles", "alpha_values", "colours", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any) -> None:
        self._result = axis.contour(
            self.x,
            self.y,
            self.z,
            levels = self.levels,
            linewidths = self.linewidths,
            linestyles = self.linestyles,
            alpha = self.alpha_values,
            colors = self.colours,
            **kwargs
        )
    @staticmethod
    def from_contours(contours: QuadContourSet, x: np.ndarray[tuple[int], np.dtype[np.floating]], y: np.ndarray[tuple[int], np.dtype[np.floating]], z: np.ndarray[tuple[int], np.dtype[np.floating]], uses_single_colour_value: bool = False) -> "CachedPlotContour":
        return CachedPlotContour(
            x = x,
            y = y,
            z = z,
            levels = tuple(contours.levels),
            linewidths = contours.get_linewidths(),
            linestyles = tuple(contours.linestyles),
            alpha_values = contours.alpha,
            colours = contours.colors if not uses_single_colour_value else tuple([contours.colors] * len(contours.levels)),
            _result = contours
        )

class CachedPlotImage(CachedPlotElement[AxesImage]):
    image = AutoProperty_NonNullable[np.ndarray[tuple[int, int], np.dtype[np.floating]]]()
    extent = AutoProperty_NonNullable[Rect]()
    origin = AutoProperty_NonNullable[Literal["upper", "lower"]](default_value = "upper")
    colourmap = AutoProperty[str|Colormap](allow_uninitialised = True)
    min_colour_value = AutoProperty[float](allow_uninitialised = True)
    max_colour_value = AutoProperty[float](allow_uninitialised = True)
    alpha = AutoProperty[np.ndarray[tuple[int, int], np.dtype[np.floating]]](allow_uninitialised = True)
    def __init__(self, **kwargs):
        super().__init__("image", "extent", "origin", "colourmap", "alpha", **kwargs)
    def render(self, figure: Figure, axis: Axes, *args: Any, **kwargs: Any):
        self._result = axis.imshow(
            self.image,
            extent = self.extent.extent,
            origin = self.origin,
            cmap = self.colourmap,
            vmin = self.min_colour_value,
            vmax = self.max_colour_value,
            alpha = self.alpha,
            **kwargs
        )
    @staticmethod
    def from_image(image: AxesImage) -> "CachedPlotImage":
        return CachedPlotImage(
            image = image.get_array(),
            extent = Rect.create_from_limits(*image.get_extent()),
            origin = image.origin,
            colourmap = image.get_cmap(),
            min_colour_value = image.get_clim()[0],
            max_colour_value = image.get_clim()[1],
            alpha = image.get_alpha()
        )

class CachedPlotText(CachedPlotElement[Text]):
    text          = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    x             = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    y             = AutoProperty_NonNullable[np.ndarray[tuple[int], np.dtype[np.floating]]]()
    font          = AutoProperty_NonNullable[CachedPlotFontInfo]()
    alpha         = AutoProperty_NonNullable[float](default_value = 1.0)
    box_colour    = AutoProperty[ColorType](allow_uninitialised = True)
    border_colour = AutoProperty[ColorType](allow_uninitialised = True)
    def __init__(self, **kwargs):
        super().__init__("text", "x", "y", "font", "alpha", "box_colour", "border_colour", **kwargs)
        self.font = CachedPlotFontInfo()
    def render(self, figure: Figure, axis: Axes, default_font: CachedPlotFontInfo, *args: Any, **kwargs: Any) -> None:
        self._result = axis.text(
            x           = self.x,
            y           = self.y,
            s           = self.text,
            **self.font.with_default(default_font).fontdict,
            alpha       = self.alpha,
            bbox        = dict(facecolor = self.box_colour, edgecolor = self.border_colour) if (self.box_colour is not None or self.border_colour is not None) else None,
            **kwargs,
        )
    @staticmethod
    def from_text(text: Text) -> "CachedPlotText":
        coords: np.ndarray[tuple[int, int], np.dtype[np.floating]] = text.get_xydata()
        return CachedPlotText(
            x         = coords[:, 0],
            y         = coords[:, 1],
            label     = text.get_label(),
            colour    = text.get_color(),
            linestyle = text.get_linestyle(),
            linewidth = text.get_linewidth(),
            alpha     = text.get_alpha(),
        )

class CachedPlotPie(CachedPlotElement[tuple[list[Wedge], list[Text]] | tuple[list[Wedge], list[Text], list[Text]]]):
    values              = AutoProperty_NonNullable[Sequence[float]|Sequence[str]]()
    colours             = AutoProperty_NonNullable[Sequence[ColorType]|Sequence[str]]()
    texture             = AutoProperty_NonNullable[Sequence[Literal["/","\\","|","-","+", "x", "o", "O", ".", "*"]]]()
    shadow              = AutoProperty_NonNullable[bool](default_value = False)
    labels              = AutoProperty_NonNullable[Sequence[str]]()
    label_distance      = AutoProperty[float](default_value = 1.1, allow_uninitialised = True)
    rotate_labels       = AutoProperty_NonNullable[bool](default_value = False)
    percentage_format   = AutoProperty[str|CacheableFunction](allow_uninitialised = True)
    percentage_distance = AutoProperty_NonNullable[float](default_value = 0.6)
    centre              = AutoProperty_NonNullable[tuple[float,float]](default_value = (0, 0))
    radius              = AutoProperty_NonNullable[float](default_value = 1.0)
    start_angle         = AutoProperty_NonNullable[float](default_value = 0.0)
    segment_rotation    = AutoProperty_NonNullable[Literal["clockwise", "anticlockwise"]](default_value = "anticlockwise")
    wedge_properties    = AutoProperty[dict](allow_uninitialised = True)
    explode_distance    = AutoProperty[Sequence[float]|Sequence[str]](allow_uninitialised = True)
    font                = AutoProperty_NonNullable[CachedPlotFontInfo]()
    hide_axes           = AutoProperty_NonNullable[bool](default_value = True)
    ensure_complete_pie = AutoProperty_NonNullable[bool](default_value = True)
    labled_data         = AutoProperty[dict](allow_uninitialised = True)
    def __init__(self, **kwargs):
        super().__init__("values", "labels", "colours", "texture", "shadow", "label_distance", "percentage_distance", "explode_distance", "percentage_format", "wedge_properties", "font", **kwargs)
        self.font = CachedPlotFontInfo()
    def render(self, figure: Figure, axis: Axes, default_font: CachedPlotFontInfo, *args: Any, **kwargs: Any):
        if not self.ensure_complete_pie and sum(self.values) > 1:
            raise ValueError("The sum of the values must not exceed 1 when ensure_complete_pie is False.")
        self._result = axis.pie(
            x             = self.values,
            explode       = self.explode_distance,
            labels        = self.labels,
            colors        = self.colours,
            autopct       = self.percentage_format,
            pctdistance   = self.percentage_distance,
            shadow        = self.shadow,
            labeldistance = self.label_distance,
            startangle    = self.start_angle,
            radius        = self.radius,
            counterclock  = self.segment_rotation == "anticlockwise",
            wedgeprops    = self.wedge_properties,
            textprops     = self.font.with_default(default_font).fontdict,
            center        = self.centre,
            frame         = not self.hide_axes,
            rotatelabels  = self.rotate_labels,
            normalize     = self.ensure_complete_pie,
            hatch         = self.texture,
            data         = self.labled_data,
            **kwargs
        )
    @property
    def fractions(self) -> Sequence[float]:
        total = sum(self.values)
        return [value / total for value in self.values]
    @property
    def percentages(self) -> Sequence[float]:
        return [value * 100 for value in self.fractions]
