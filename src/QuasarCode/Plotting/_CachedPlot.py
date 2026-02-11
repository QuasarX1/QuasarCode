import math
from typing import Any, Literal

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.axes._secondary_axes import SecondaryAxis

from ..Data._Rect import Rect
from ..IO.Caching._CacheableList import CacheableList
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable
from ..Tools._CacheableFunction import CacheableFunction
from ._CachedPlotFontInfo import CachedPlotFontInfo
from ._CachedPlotElements import CachedPlotElement, CachedPlotColourbar

class CachedPlot(CacheableStruct):
    title = AutoProperty[str](allow_uninitialised = True)
    plot_elements = AutoProperty_NonNullable[dict[str, CachedPlotElement]]()
    colourbars = AutoProperty_NonNullable[dict[str, CachedPlotColourbar]]()
    extent = AutoProperty_NonNullable[Rect]()
    aspect = AutoProperty[Literal["auto", "equal"]|float](allow_uninitialised = True)
    aspect_adjustable = AutoProperty[Literal["box", "datalim"]](allow_uninitialised = True)
    aspect_anchor = AutoProperty[Literal["C", "N", "NE", "E", "SE", "S", "SW", "W", "N"]|tuple[float, float]](allow_uninitialised = True)
    x_axis_label = AutoProperty[str](allow_uninitialised = True)
    y_axis_label = AutoProperty[str](allow_uninitialised = True)
    flip_x = AutoProperty_NonNullable[bool](default_value = False)
    flip_y = AutoProperty_NonNullable[bool](default_value = False)
    show_legend = AutoProperty_NonNullable[bool](default_value = False)
    show_x_ticks = AutoProperty_NonNullable[bool](default_value = True)
    show_y_ticks = AutoProperty_NonNullable[bool](default_value = True)
    show_x_ticks_on_other_side = AutoProperty_NonNullable[bool](default_value = False)
    show_y_ticks_on_other_side = AutoProperty_NonNullable[bool](default_value = False)
    show_x_tick_labels = AutoProperty_NonNullable[bool](default_value = True)
    show_y_tick_labels = AutoProperty_NonNullable[bool](default_value = True)
    show_x_tick_labels_on_other_side = AutoProperty_NonNullable[bool](default_value = False)
    show_y_tick_labels_on_other_side = AutoProperty_NonNullable[bool](default_value = False)
    x_ticks_inside = AutoProperty_NonNullable[bool](default_value = False)
    y_ticks_inside = AutoProperty_NonNullable[bool](default_value = False)
    alt_x_axis_functions = AutoProperty[CacheableList[CacheableFunction]](allow_uninitialised = True)
    alt_y_axis_functions = AutoProperty[CacheableList[CacheableFunction]](allow_uninitialised = True)
    alt_x_axis_label = AutoProperty[str](allow_uninitialised = True)
    alt_y_axis_label = AutoProperty[str](allow_uninitialised = True)
    _alt_x_axis = AutoProperty[SecondaryAxis](allow_uninitialised = True)
    _alt_y_axis = AutoProperty[SecondaryAxis](allow_uninitialised = True)
    show_alt_x_ticks = AutoProperty_NonNullable[bool](default_value = True)
    show_alt_y_ticks = AutoProperty_NonNullable[bool](default_value = True)
    show_alt_x_tick_labels = AutoProperty_NonNullable[bool](default_value = True)
    show_alt_y_tick_labels = AutoProperty_NonNullable[bool](default_value = True)
    alt_x_ticks_inside = AutoProperty_NonNullable[bool](default_value = False)
    alt_y_ticks_inside = AutoProperty_NonNullable[bool](default_value = False)
    default_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    title_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    x_axis_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    y_axis_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    alt_x_axis_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    alt_y_axis_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    x_tick_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    y_tick_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    alt_x_tick_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    alt_y_tick_label_font = AutoProperty_NonNullable[CachedPlotFontInfo]()
    def __init__(self, **kwargs):
        super().__init__(
            cacheable_attributes = ("title", "plot_elements", "colourbars", "extent", "aspect", "aspect_adjustable", "aspect_anchor", "x_axis_label", "y_axis_label", "flip_x", "flip_y", "show_legend", "show_x_ticks", "show_y_ticks", "show_x_ticks_on_other_side", "show_y_ticks_on_other_side", "show_x_tick_labels", "show_y_tick_labels", "show_x_tick_labels_on_other_side", "show_y_tick_labels_on_other_side", "x_ticks_inside", "y_ticks_inside", "alt_x_axis_functions", "alt_y_axis_functions", "alt_x_axis_label", "alt_y_axis_label", "show_alt_x_ticks", "show_alt_y_ticks", "show_alt_x_tick_labels", "show_alt_y_tick_labels", "alt_x_ticks_inside", "alt_y_ticks_inside"),
            **kwargs
        )
        self.plot_elements = {}
        self.colourbars = {}
        self.default_font = CachedPlotFontInfo()
        self.title_font = CachedPlotFontInfo()
        self.x_axis_label_font = CachedPlotFontInfo()
        self.y_axis_label_font = CachedPlotFontInfo()
        self.alt_x_axis_label_font = CachedPlotFontInfo()
        self.alt_y_axis_label_font = CachedPlotFontInfo()
        self.x_tick_label_font = CachedPlotFontInfo()
        self.y_tick_label_font = CachedPlotFontInfo()
        self.alt_x_tick_label_font = CachedPlotFontInfo()
        self.alt_y_tick_label_font = CachedPlotFontInfo()
    
    def __check_element_name_is_new(self, name: str) -> bool:
        return name not in self.plot_elements

    def add_element(self, name: str, element: CachedPlotElement) -> None:
        if not self.__check_element_name_is_new(name):
            raise KeyError(f"An element already exists with the name \"{name}\".")
        self.plot_elements[name] = element

    def add_colourbar(self, name: str, colourbar: CachedPlotColourbar) -> None:
        if name in self.colourbars:
            raise KeyError(f"A colourbar already exists with the name \"{name}\".")
        if self.__check_element_name_is_new(colourbar.target_element):
            raise KeyError(f"No element exists with the target name \"{colourbar.target_element}\".")
        self.colourbars[name] = colourbar

    def render(self, figure: Figure, axis: Axes, figure_default_font: Optional[CachedPlotFontInfo] = None, forward_kwargs: dict[str, dict[str, Any]]|None = None, forward_colourbar_kwargs: dict[str, dict[str, Any]]|None = None) -> None:
        if forward_kwargs is None:
            forward_kwargs = {}
        if forward_colourbar_kwargs is None:
            forward_colourbar_kwargs = {}
        for element in self.plot_elements:
            self.plot_elements[element].render(figure, axis, default_font = self.default_font.with_default(figure_default_font), **forward_kwargs.get(element, {}))

        for name, colourbar in self.colourbars.items():
            target: object
            if colourbar.target_element in self.plot_elements:
                target = self.plot_elements[colourbar.target_element]._result
            else:
                raise RuntimeError(f"Unable to locate target for colourbar \"{name}\".")
            colourbar.render(figure, axis, target, default_font = self.default_font.with_default(figure_default_font), **forward_colourbar_kwargs.get(name, {}))

        if self.title is not None:
            axis.set_title(self.title, **self.title_font.with_default(self.default_font).with_default(figure_default_font).fontdict)

        if self.x_axis_label is not None:
            axis.set_xlabel(self.x_axis_label, **self.x_axis_label_font.with_default(self.default_font).with_default(figure_default_font).fontdict)
        if self.y_axis_label is not None:
            axis.set_ylabel(self.y_axis_label, **self.y_axis_label_font.with_default(self.default_font).with_default(figure_default_font).fontdict)

        x_tick_label_font = self.x_tick_label_font.with_default(self.default_font).with_default(figure_default_font)
        axis.tick_params(
            axis            = "x",
            bottom          = self.show_x_ticks,
            top             = self.show_x_ticks_on_other_side and self.alt_x_axis_functions is None,
            direction       = "in" if self.x_ticks_inside else "out",
            labelbottom     = self.show_x_tick_labels,
            labeltop        = self.show_x_tick_labels_on_other_side,
            labelsize       = x_tick_label_font.size,
            labelcolor      = x_tick_label_font.color,
            labelfontfamily = x_tick_label_font.family,
        )

        y_tick_label_font = self.y_tick_label_font.with_default(self.default_font).with_default(figure_default_font)
        axis.tick_params(
            axis            = "y",
            left            = self.show_y_ticks,
            right           = self.show_y_ticks_on_other_side and self.alt_y_axis_functions is None,
            direction       = "in" if self.y_ticks_inside else "out",
            labelleft       = self.show_y_tick_labels,
            labelright      = self.show_y_tick_labels_on_other_side,
            labelsize       = y_tick_label_font.size,
            labelcolor      = y_tick_label_font.color,
            labelfontfamily = y_tick_label_font.family,
        )

        axis.set_xlim(self.extent.extent[0:2] if not self.flip_x else self.extent.extent[1::-1])
        axis.set_ylim(self.extent.extent[2:4] if not self.flip_y else self.extent.extent[3:1:-1])

        if self.alt_x_axis_functions is not None:
            self._alt_x_axis = axis.secondary_xaxis(
                "top",
                functions = tuple(self.alt_x_axis_functions)
            )
            if self.alt_x_axis_label is not None:
                self._alt_x_axis.set_xlabel(self.alt_x_axis_label, **self.alt_x_axis_label_font.with_default(self.default_font).with_default(figure_default_font).fontdict)
            alt_x_tick_label_font = self.alt_x_tick_label_font.with_default(self.x_tick_label_font).with_default(self.default_font).with_default(figure_default_font)
            self._alt_x_axis.tick_params(
                axis            = "x",
                top             = self.show_alt_x_ticks,
                direction       = "in" if self.alt_x_ticks_inside else "out",
                labeltop        = self.show_alt_x_tick_labels,
                labelsize       = alt_x_tick_label_font.size,
                labelcolor      = alt_x_tick_label_font.color,
                labelfontfamily = alt_x_tick_label_font.family,
            )

        if self.alt_y_axis_functions is not None:
            self._alt_y_axis = axis.secondary_yaxis(
                "right",
                functions = tuple(self.alt_y_axis_functions)
            )
            if self.alt_y_axis_label is not None:
                self._alt_y_axis.set_xlabel(self.alt_y_axis_label, **self.alt_y_axis_label_font.with_default(self.default_font).with_default(figure_default_font).fontdict)
            alt_y_tick_label_font = self.alt_y_tick_label_font.with_default(self.y_tick_label_font).with_default(self.default_font).with_default(figure_default_font)
            self._alt_y_axis.tick_params(
                axis            = "y",
                right           = self.show_alt_y_ticks,
                direction       = "in" if self.alt_y_ticks_inside else "out",
                labelright      = self.show_alt_y_tick_labels,
                labelsize       = alt_y_tick_label_font.size,
                labelcolor      = alt_y_tick_label_font.color,
                labelfontfamily = alt_y_tick_label_font.family,
            )

        if self.aspect is not None:
            axis.set_aspect(self.aspect, adjustable = self.aspect_adjustable, anchor = self.aspect_anchor)

        if self.show_legend:
            axis.legend()
