from typing import Union, List, Tuple, Dict, cast

from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt

from QuasarCode.Data import Rect
from QuasarCode.Plotting import CachedPlotFactory, CachedPlot, CachedPlotLine, CachedPlotScatter, CachedPlotErrorbar, CachedPlotHexbin
from QuasarCode.IO.Caching import CacheTargetFactory, CacheTarget

class Test_CachedPlot(object):

    def test_line(self):

        plot_factory = CachedPlotFactory(".")
        assert isinstance(plot_factory, CachedPlotFactory)

        plot_data = plot_factory.new(Rect.create_from_size(0, 0, 10, 10))
        assert isinstance(plot_data, CachedPlot)
        assert plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert plot_data.flip_x is False

        cache_factory = CacheTargetFactory("test_cache/Test_CachedPlot/test_line/{file}.pickle", "file")

        cache = cache_factory.new(file = "test_line")

        line_coords = (
            [0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10],
            [0, 2, 1, 4, 3, 6, 5, 8, 7, 10,  9]
        )

        fig = plt.figure()
        ax = fig.gca()
        mplt_line_object = plt.plot(*line_coords, label = "Line", color = "blue", linestyle = "-")[0]
        plt.legend()

        plot_data.add_element("line", CachedPlotLine.from_line(mplt_line_object))
        plot_data.render(fig, ax)

        re_rendered_test_line: Line2D = plot_data.plot_elements["line"].result
        assert np.all(re_rendered_test_line.get_xydata() == mplt_line_object.get_xydata())

        plot_factory.save(plot_data, cache)

        loaded_plot_data: CachedPlot = plot_factory.load(cache)
        assert isinstance(loaded_plot_data, CachedPlot)
        assert loaded_plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert loaded_plot_data.flip_x is False

        loaded_plot_data.render(fig, ax)
        loaded_re_rendered_test_line: Line2D = loaded_plot_data.plot_elements["line"].result
        assert np.all(loaded_re_rendered_test_line.get_xydata() == mplt_line_object.get_xydata())

    def test_scatter(self):

        plot_factory = CachedPlotFactory(".")
        assert isinstance(plot_factory, CachedPlotFactory)

        plot_data = plot_factory.new(Rect.create_from_size(0, 0, 10, 10))
        assert isinstance(plot_data, CachedPlot)
        assert plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert plot_data.flip_x is False

        cache_factory = CacheTargetFactory("test_cache/Test_CachedPlot/test_line/{file}.pickle", "file")

        cache = cache_factory.new(file = "test_line")

        line_coords = (
            [0, 1, 2, 3, 4, 5, 6, 7, 8,  9, 10],
            [0, 2, 1, 4, 3, 6, 5, 8, 7, 10,  9]
        )

        fig = plt.figure()
        ax = fig.gca()
        mplt_scatter_object = plt.scatter(*line_coords, label = "Scatter", color = "blue", marker = "^")
        plt.legend()

        plot_data.add_element("scatter", CachedPlotScatter.from_points(mplt_scatter_object))
        plot_data.render(fig, ax)

        re_rendered_test_scatter: PathCollection = plot_data.plot_elements["scatter"].result
        assert np.all(re_rendered_test_scatter.get_offsets() == mplt_scatter_object.get_offsets())

        plot_factory.save(plot_data, cache)

        loaded_plot_data: CachedPlot = plot_factory.load(cache)
        assert isinstance(loaded_plot_data, CachedPlot)
        assert loaded_plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert loaded_plot_data.flip_x is False

        loaded_plot_data.render(fig, ax)
        loaded_re_rendered_test_scatter: PathCollection = loaded_plot_data.plot_elements["scatter"].result
        assert np.all(loaded_re_rendered_test_scatter.get_offsets() == mplt_scatter_object.get_offsets())
