from typing import Any, Optional, Literal

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.artist import Artist
from matplotlib.typing import ColorType

from ..Data._Rect import Rect
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable
from ._CachedPlotFontInfo import CachedPlotFontInfo
from ._CachedPlotElements import CachedPlotElement

class CachedPlotLegendBoxProperties(CacheableStruct):
    show             = AutoProperty[bool ](allow_uninitialised = True)
    round_corners    = AutoProperty[bool ](allow_uninitialised = True)
    shadow           = AutoProperty[bool ](allow_uninitialised = True)
    alpha            = AutoProperty[float](allow_uninitialised = True)
    face_colour      = AutoProperty[ColorType|Literal["inherit"]](allow_uninitialised = True)
    edge_colour      = AutoProperty[ColorType|Literal["inherit"]](allow_uninitialised = True)
    padding          = AutoProperty[float](allow_uninitialised = True) # in multiples of the font-size
    margin           = AutoProperty[float](allow_uninitialised = True) # in units of font-size
    def __init__(self, **kwargs):
        super().__init__(
            cacheable_attributes = ["show", "round_corners", "shadow", "alpha", "face_colour", "edge_colour", "padding", "margin"],
            **kwargs
        )

class CachedPlotCustomLegend(CacheableStruct):
    title                           = AutoProperty            [str                          ](allow_uninitialised = True)
    element_targets                 = AutoProperty_NonNullable[dict[str,str|tuple[str,str]] ]() # Label : target element | (target plot, target element)
    reverse_order                   = AutoProperty_NonNullable[bool                         ](default_value = False)
    columns                         = AutoProperty_NonNullable[int                          ](default_value = 1)
    position                        = AutoProperty_NonNullable[Literal["best", "upper left", "upper center", "upper right", "center left", "center", "center right", "lower left", "lower center", "lower right"]|tuple[float, float]](default_value = "best")
    anchor_region                   = AutoProperty            [Rect                         ](allow_uninitialised = True) # Max. one of these \/ can be set
    anchor                          = AutoProperty            [tuple[int,int]               ](allow_uninitialised = True) # Max. one of these /\ can be set
    anchor_space                    = AutoProperty            [Literal["figure-space", "axis-space", "axis-data-space"]](allow_uninitialised = True)
    label_font                      = AutoProperty_NonNullable[CachedPlotFontInfo           ]()
    label_colours                   = AutoProperty            [str|Literal["linecolor", "markerfacecolor", "markeredgecolor"]|list[str|Literal["linecolor", "markerfacecolor", "markeredgecolor"]]](allow_uninitialised = True)
    title_font                      = AutoProperty_NonNullable[CachedPlotFontInfo           ]()
    alignment                       = AutoProperty_NonNullable[Literal["left", "center", "right"]](default_value = "center")

    line_render_points              = AutoProperty            [int                          ](allow_uninitialised = True)
    scatter_render_points           = AutoProperty            [int                          ](allow_uninitialised = True)
    scatter_render_points_y_offsets = AutoProperty_NonNullable[list[float]                  ](default_value = [0.375, 0.5, 0.3125]) # Relative to the font height (0 -> 1)
    marker_scale                    = AutoProperty            [float                        ](allow_uninitialised = True)
    marker_location                 = AutoProperty_NonNullable[Literal["left", "right"]     ](default_value = "left")
    vertical_spacing                = AutoProperty            [float                        ](allow_uninitialised = True) # in units of font-size
    horizontal_spacing              = AutoProperty            [float                        ](allow_uninitialised = True) # in units of font-size
    handle_length                   = AutoProperty            [float                        ](allow_uninitialised = True) # in units of font-size
    handle_height                   = AutoProperty            [float                        ](allow_uninitialised = True) # in units of font-size
    handle_text_space               = AutoProperty            [float                        ](allow_uninitialised = True) # in units of font-size

    box                             = AutoProperty_NonNullable[CachedPlotLegendBoxProperties]()
    expand_into_horizontal_space    = AutoProperty_NonNullable[bool                         ](default_value = False)
    mouse_draggable                 = AutoProperty_NonNullable[bool                         ](default_value = False)

    def __init__(self, **kwargs):
        super().__init__(
            cacheable_attributes = [
                "title", "element_targets", "reverse_order", "columns", "position",
                "anchor_region", "anchor", "anchor_space", "label_font", "label_colours",
                "title_font", "alignment", "line_render_points", "scatter_render_points",
                "scatter_render_points_y_offsets", "marker_scale", "marker_location",
                "vertical_spacing", "horizontal_spacing", "handle_length", "handle_height",
                "handle_text_space", "box", "expand_into_horizontal_space", "mouse_draggable"
            ],
            **kwargs
        )
        if "element_targets" not in kwargs:
            self.element_targets = {}
        if "label_font" not in kwargs:
            self.label_font = CachedPlotFontInfo()
        if "title_font" not in kwargs:
            self.title_font = CachedPlotFontInfo()
        if "box" not in kwargs:
            self.box = CachedPlotLegendBoxProperties()

    def render(self, figure: Figure, axis: Axes|None, default_font: CachedPlotFontInfo, plot_elements: Optional[dict[str, CachedPlotElement]] = None, elements_by_figure_plot: Optional[dict[str, dict[str, CachedPlotElement]]] = None, *args: Any, **kwargs: Any) -> None:

        if plot_elements is None and elements_by_figure_plot is None:
            raise ValueError("At least one of plot_elements or elements_by_figure_plot must be provided to render a CachedPlotCustomLegend.")
        
        if self.anchor is None and self.anchor_region is not None:
            raise ValueError("Only one of anchor or anchor_region may be set.")
        
        if self.anchor_space is not None and self.anchor_space != "figure-space" and axis is None:
            raise ValueError("anchor_space cannot be set to a value other than 'figure-space' if axis is not provided.")
        
        anchor_transform = None if self.anchor_space is None else figure.transFigure if self.anchor_space == "figure-space" else axis.transAxes if self.anchor_space == "axis-space" else axis.transData

        artists = []
        labels = []
        for label, target in self.element_targets.items():
            target_plot: str|None
            target_element: str
            artist: Artist
            if isinstance(target, str):
                target_plot = None
                target_element = target
            else:
                target_plot = target[0]
                target_element = target[1]
            if target_plot is None:
                if plot_elements is None:
                    raise ValueError("plot_elements must be provided to render a CachedPlotCustomLegend with element_targets that do not specify a target plot.")
                artist = plot_elements[target_element]._result
            else:
                if elements_by_figure_plot is None:
                    raise ValueError("elements_by_figure_plot must be provided to render a CachedPlotCustomLegend with element_targets that specify a target plot.")
                artist = elements_by_figure_plot[target_plot][target_element]._result
            artists.append(artist)
            labels.append(label)

        (axis if axis is not None else figure).legend(
            handles              = artists,
            labels               = labels,
            loc                  = self.position,
            bbox_to_anchor       = self.anchor if self.anchor is not None else self.anchor_region.extent if self.anchor_region is not None else None,
            ncols                = self.columns,
            prop                 = self.label_font.with_default(default_font).fontproperties,
            labelcolor           = self.label_colours if self.label_colours is not None else self.label_font.with_default(default_font).colour if (self.label_font.colour is not None or default_font.colour is not None) else default_font.colour,
            numpoints            = self.line_render_points,
            scatterpoints        = self.scatter_render_points,
            scatteryoffsets      = self.scatter_render_points_y_offsets,
            markerscale          = self.marker_scale,
            markerfirst          = self.marker_location == "first",
            reverse              = self.reverse_order,
            frameon              = self.box.show,
            fancybox             = self.box.round_corners,
            shadow               = self.box.shadow,
            framealpha           = self.box.alpha,
            facecolor            = self.box.face_colour,
            edgecolor            = self.box.edge_colour,
            mode                 = "expand" if self.expand_into_horizontal_space else None,
            bbox_transform       = anchor_transform,
            title                = self.title,
            title_fontproperties = self.title_font.with_default(self.label_font).with_default(default_font).fontproperties,
            alignment            = self.alignment,
            borderpad            = self.box.padding,
            labelspacing         = self.vertical_spacing,
            handlelength         = self.handle_length,
            handleheight         = self.handle_height,
            handletextpad        = self.handle_text_space,
            borderaxespad        = self.box.margin,
            columnspacing        = self.horizontal_spacing,
#            handler_map          =,
            draggable            =self.mouse_draggable,
        )