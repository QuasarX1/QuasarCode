from typing import Sequence, Literal

from matplotlib.font_manager import FontProperties

from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty

class CachedPlotFontInfo(CacheableStruct):
    size    = AutoProperty[float|Literal["xx-small","x-small","small","medium","large","x-large","xx-large"]](allow_uninitialised = True) # Matplotlib default is 10.0
    family  = AutoProperty[Sequence[str]](allow_uninitialised = True)
    style   = AutoProperty[str          ](allow_uninitialised = True)
    variant = AutoProperty[str          ](allow_uninitialised = True)
    weight  = AutoProperty[str|float    ](allow_uninitialised = True)
    stretch = AutoProperty[str          ](allow_uninitialised = True)
    def __init__(self, **kwargs):
        super().__init__("size", "family", "style", "variant", "weight", "stretch", **kwargs)

    @staticmethod
    def from_font_properties(font_properties: FontProperties) -> "CachedPlotFontInfo":
        instance = CachedPlotFontInfo()
        instance.size    = font_properties.get_size()
        instance.family  = font_properties.get_family()
        instance.style   = font_properties.get_style()
        instance.variant = font_properties.get_variant()
        instance.weight  = font_properties.get_weight()
        instance.stretch = font_properties.get_stretch()
        return instance
    
    def copy(self) -> "CachedPlotFontInfo":
        """
        Returns a shallow copy.
        """
        instance = CachedPlotFontInfo()
        if self.size is not None:
            instance.size = self.size
        if self.family is not None:
            instance.family = self.family
        if self.style is not None:
            instance.style = self.style
        if self.variant is not None:
            instance.variant = self.variant
        if self.weight is not None:
            instance.weight = self.weight
        if self.stretch is not None:
            instance.stretch = self.stretch
        return instance
    
    def with_default(self, default: "CachedPlotFontInfo") -> "CachedPlotFontInfo":
        """
        Return a new instance using the default values specified (where there are any).
        """
        instance = default.copy()
        if self.size is not None:
            instance.size = self.size
        if self.family is not None:
            instance.family = self.family
        if self.style is not None:
            instance.style = self.style
        if self.variant is not None:
            instance.variant = self.variant
        if self.weight is not None:
            instance.weight = self.weight
        if self.stretch is not None:
            instance.stretch = self.stretch
        return instance
