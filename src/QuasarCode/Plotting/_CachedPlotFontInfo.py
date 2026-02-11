from typing import Sequence

from ..Tools._Struct import CacheableStruct
from ..Tools._autoproperty import AutoProperty

class CachedPlotFontInfo(CacheableStruct):
    family  = AutoProperty[Sequence[str]](allow_uninitialised = True)
    style   = AutoProperty[str          ](allow_uninitialised = True)
    variant = AutoProperty[str          ](allow_uninitialised = True)
    weight  = AutoProperty[str|float    ](allow_uninitialised = True)
    stretch = AutoProperty[str          ](allow_uninitialised = True)