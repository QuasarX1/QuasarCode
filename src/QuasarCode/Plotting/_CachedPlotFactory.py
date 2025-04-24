from ..Data._Rect import Rect
from ._CachedPlot import CachedPlot
from ..IO.Caching._CacheTarget import CacheTarget

class CachedPlotFactory(object):
    def __init__(self, cache_directory: str) -> None:
        self.__cache_directory: str = cache_directory

    def new(self, extent: Rect) -> CachedPlot:
        return CachedPlot(extent = extent)
    
    def load(self, target: CacheTarget) -> CachedPlot:
        return target.load_object(self.__cache_directory, CachedPlot)

    def save(self, plot: CachedPlot, target: CacheTarget) -> None:
        target.save_object(self.__cache_directory, plot)
