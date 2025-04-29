from typing import Union, List, Tuple, Dict, cast

from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.contour import QuadContourSet
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt

from QuasarCode.Data import Rect
from QuasarCode.Plotting import CachedPlotFactory, CachedPlot, CachedPlotLine, CachedPlotScatter, CachedPlotErrorbar, CachedPlotHexbin, CachedPlotContour, Hexbin, Contour
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

        cache_factory = CacheTargetFactory("test_cache/Test_CachedPlot/test_scatter/{file}.pickle", "file")

        cache = cache_factory.new(file = "test_scatter")

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

    def test_hexbin(self):

        plot_factory = CachedPlotFactory(".")
        assert isinstance(plot_factory, CachedPlotFactory)

        plot_data = plot_factory.new(Rect.create_from_size(0, 0, 10, 10))
        assert isinstance(plot_data, CachedPlot)
        assert plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert plot_data.flip_x is False

        cache_factory = CacheTargetFactory("test_cache/Test_CachedPlot/test_hex/{file}.pickle", "file")

        cache = cache_factory.new(file = "test_hex")

        coords = np.random.rand(1000, 2) * 10

        fig = plt.figure()
        ax = fig.gca()
        mplt_hex_object = plt.hexbin(coords[:, 0], coords[:, 1], cmap = "viridis", gridsize = 100, extent = plot_data.extent.extent)
        plt.legend()

        plot_data.add_element("hexbin", CachedPlotHexbin.from_hexes(mplt_hex_object, plot_data.extent, 100))
        plot_data.render(fig, ax)

        re_rendered_test_hexbin: PolyCollection = plot_data.plot_elements["hexbin"].result
        assert np.all(re_rendered_test_hexbin.get_offsets() == mplt_hex_object.get_offsets())
        assert np.all(re_rendered_test_hexbin.get_array() == mplt_hex_object.get_array())
        assert np.all(re_rendered_test_hexbin.get_alpha() == mplt_hex_object.get_alpha())

        plot_factory.save(plot_data, cache)

        loaded_plot_data: CachedPlot = plot_factory.load(cache)
        assert isinstance(loaded_plot_data, CachedPlot)
        assert loaded_plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert loaded_plot_data.flip_x is False

        loaded_plot_data.render(fig, ax)
        loaded_re_rendered_test_hexbin: PolyCollection = loaded_plot_data.plot_elements["hexbin"].result
        assert np.all(loaded_re_rendered_test_hexbin.get_offsets() == mplt_hex_object.get_offsets())
        assert np.all(loaded_re_rendered_test_hexbin.get_array() == mplt_hex_object.get_array())
        assert np.all(loaded_re_rendered_test_hexbin.get_alpha() == mplt_hex_object.get_alpha())

    def test_Hexbin(self):

        plot_factory = CachedPlotFactory(".")
        assert isinstance(plot_factory, CachedPlotFactory)

        plot_data = plot_factory.new(Rect.create_from_size(0, 0, 10, 10))
        assert isinstance(plot_data, CachedPlot)
        assert plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert plot_data.flip_x is False

        cache_factory = CacheTargetFactory("test_cache/Test_CachedPlot/test_hex/{file}.pickle", "file")

        cache = cache_factory.new(file = "test_hex_from_Hexbin")

        coords = np.random.rand(1000, 2) * 10

        hexbin_object = Hexbin(coords[:, 0], coords[:, 1])
        hexbin_object.plot_hexbin(extent = plot_data.extent, gridsize = 100, colourmap = "viridis")
        mplt_hex_object = hexbin_object.data.result
        assert isinstance(mplt_hex_object, PolyCollection)

        fig = plt.figure()
        ax = fig.gca()

        plot_data.add_element("hexbin", hexbin_object.data)
        plot_data.render(fig, ax)

        re_rendered_test_hexbin: PolyCollection = plot_data.plot_elements["hexbin"].result
        assert isinstance(re_rendered_test_hexbin, PolyCollection)
        assert np.all(re_rendered_test_hexbin.get_offsets() == mplt_hex_object.get_offsets())
        assert np.all(re_rendered_test_hexbin.get_array() == mplt_hex_object.get_array())
        assert np.all(re_rendered_test_hexbin.get_alpha() == mplt_hex_object.get_alpha())

        plot_factory.save(plot_data, cache)

        loaded_plot_data: CachedPlot = plot_factory.load(cache)
        assert isinstance(loaded_plot_data, CachedPlot)
        assert loaded_plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert loaded_plot_data.flip_x is False

        loaded_plot_data.render(fig, ax)
        loaded_re_rendered_test_hexbin: PolyCollection = loaded_plot_data.plot_elements["hexbin"].result
        assert isinstance(loaded_re_rendered_test_hexbin, PolyCollection)
        assert np.all(loaded_re_rendered_test_hexbin.get_offsets() == mplt_hex_object.get_offsets())
        assert np.all(loaded_re_rendered_test_hexbin.get_array() == mplt_hex_object.get_array())
        assert np.all(loaded_re_rendered_test_hexbin.get_alpha() == mplt_hex_object.get_alpha())

    def test_Contour(self):

        plot_factory = CachedPlotFactory(".")
        assert isinstance(plot_factory, CachedPlotFactory)

        plot_data = plot_factory.new(Rect.create_from_size(0, 0, 10, 10))
        assert isinstance(plot_data, CachedPlot)
        assert plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert plot_data.flip_x is False

        cache_factory = CacheTargetFactory("test_cache/Test_CachedPlot/test_hex/{file}.pickle", "file")

        cache = cache_factory.new(file = "test_hex_from_Hexbin")

        coords = np.random.rand(1000, 2) * 10

        contour_object = Contour(coords[:, 0], coords[:, 1])

        contour_object.generate(gridsize = 100) # Run this early to get the min/max levels

        contour_object.add_contours(
            (contour_object.max_level - contour_object.min_level) / 4,
            (contour_object.max_level - contour_object.min_level) / 2,
            (contour_object.max_level - contour_object.min_level) * 3/4
        )

        lvl0, lvl1, lvl2 = sorted(contour_object.contour_levels)
        assert lvl0 == (contour_object.max_level - contour_object.min_level) / 4
        assert lvl1 == (contour_object.max_level - contour_object.min_level) / 2
        assert lvl2 == (contour_object.max_level - contour_object.min_level) * 3/4

        contour_object.set_colour(lvl2, "black")
        contour_object.set_linestyle(lvl2, "-")

        contour_object.set_colour(lvl1, "blue")
        contour_object.set_linestyle(lvl1, "--")

        contour_object.set_colour(lvl0, "green")
        contour_object.set_linestyle(lvl0, ":")

        fig = plt.figure()
        ax = fig.gca()

        mplt_hex_object = contour_object.plot(ax)
        assert isinstance(mplt_hex_object, QuadContourSet)
        assert isinstance(contour_object.plotting_result, QuadContourSet)

        plot_data.add_element("contour", contour_object.data)
        plot_data.render(fig, ax)

        re_rendered_test_contour: QuadContourSet = plot_data.plot_elements["contour"].result
        assert isinstance(re_rendered_test_contour, QuadContourSet)
        assert np.all(re_rendered_test_contour.levels == mplt_hex_object.levels)
        assert np.all(re_rendered_test_contour.alpha == mplt_hex_object.alpha)
        assert np.all(re_rendered_test_contour.colors == mplt_hex_object.colors)
        assert np.all(re_rendered_test_contour.linestyles == mplt_hex_object.linestyles)
        assert np.all(re_rendered_test_contour.get_linewidth() == mplt_hex_object.get_linewidth())

        plot_factory.save(plot_data, cache)

        loaded_plot_data: CachedPlot = plot_factory.load(cache)
        assert isinstance(loaded_plot_data, CachedPlot)
        assert loaded_plot_data.extent == Rect.create_from_size(0, 0, 10, 10)
        assert loaded_plot_data.flip_x is False

        loaded_plot_data.render(fig, ax)
        loaded_re_rendered_test_contour: QuadContourSet = loaded_plot_data.plot_elements["contour"].result
        assert isinstance(loaded_re_rendered_test_contour, QuadContourSet)
        assert np.all(loaded_re_rendered_test_contour.levels == mplt_hex_object.levels)
        assert np.all(loaded_re_rendered_test_contour.alpha == mplt_hex_object.alpha)
        assert np.all(loaded_re_rendered_test_contour.colors == mplt_hex_object.colors)
        assert np.all(loaded_re_rendered_test_contour.linestyles == mplt_hex_object.linestyles)
        assert np.all(loaded_re_rendered_test_contour.get_linewidth() == mplt_hex_object.get_linewidth())

