from typing import Any

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from ..Data._Rect import Rect
from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty, AutoProperty_NonNullable
from ._CachedPlotElements import CachedPlotElement, CachedPlotColourbar

class CachedPlot(CacheableStruct):
    plot_elements = AutoProperty_NonNullable[dict[str, CachedPlotElement]]()
    colourbars = AutoProperty_NonNullable[dict[str, CachedPlotColourbar]]()
    extent = AutoProperty_NonNullable[Rect]()
    x_axis_label = AutoProperty[str](allow_uninitialised = True)
    y_axis_label = AutoProperty[str](allow_uninitialised = True)
    flip_x = AutoProperty_NonNullable[bool](default_value = False)
    flip_y = AutoProperty_NonNullable[bool](default_value = False)
    show_legend = AutoProperty_NonNullable[bool](default_value = False)
    def __init__(self, **kwargs):
        super().__init__(
            cacheable_attributes = ("plot_elements", "colourbars", "extent", "x_axis_label", "y_axis_label", "flip_x", "flip_y", "show_legend"),
            **kwargs
        )
        self.plot_elements = {}
        self.colourbars = {}
    
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

    def render(self, figure: Figure, axis: Axes, forward_kwargs: dict[str, dict[str, Any]]|None = None, forward_colourbar_kwargs: dict[str, dict[str, Any]]|None = None) -> None:
        if forward_kwargs is None:
            forward_kwargs = {}
        if forward_colourbar_kwargs is None:
            forward_colourbar_kwargs = {}
        for element in self.plot_elements:
            self.plot_elements[element].render(figure, axis, **forward_kwargs.get(element, {}))

        for name, colourbar in self.colourbars.items():
            target: object
            if colourbar.target_element in self.plot_elements:
                target = self.plot_elements[colourbar.target_element]._result
            else:
                raise RuntimeError(f"Unable to locate target for colourbar \"{name}\".")
            colourbar.render(figure, axis, target, **forward_colourbar_kwargs.get(name, {}))

        if self.x_axis_label is not None:
            axis.set_xlabel(self.x_axis_label)
        if self.y_axis_label is not None:
            axis.set_ylabel(self.y_axis_label)
        
        axis.set_xlim(self.extent.extent[0:2] if not self.flip_x else self.extent.extent[1:-1:-1])
        axis.set_ylim(self.extent.extent[2:4] if not self.flip_y else self.extent.extent[3:1:-1])

        if self.show_legend:
            axis.legend()
