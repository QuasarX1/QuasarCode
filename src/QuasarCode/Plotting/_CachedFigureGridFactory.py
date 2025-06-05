from ..Data._Rect import Rect
from ._CachedFigureGrid import CachedFigureGrid
from ..IO.Caching._CacheTarget import CacheTarget

class CachedFigureGridFactory(object):
    def __init__(self, cache_directory: str) -> None:
        self.__cache_directory: str = cache_directory

    def new(self, extent: Rect) -> CachedFigureGrid:
        return CachedFigureGrid(extent = extent)

    def load(self, target: CacheTarget) -> CachedFigureGrid:
        return target.load_object(self.__cache_directory, CachedFigureGrid)

    def save(self, figure_grid: CachedFigureGrid, target: CacheTarget) -> None:
        target.save_object(self.__cache_directory, figure_grid)
