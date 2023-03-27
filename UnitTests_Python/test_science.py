import pytest
from decimal import Decimal
import numpy as np

##from QuasarCode.Science.graph import Figure
##from QuasarCode.Science.data import errorString, sigFig
from QuasarCode.Science import Figure, error_string, sig_fig

class TestClass_Science(object):
    def test_sig_fig(self):
        assert Decimal(436784329.828746) == sig_fig(436784329.828746, 15), "Rounding to 15 sig fig failed."
        assert Decimal(436784329.82874) == sig_fig(436784329.828746, 14), "Rounding to 14 sig fig failed."
        assert Decimal(436784329.8287) == sig_fig(436784329.828746, 13), "Rounding to 13 sig fig failed."
        assert Decimal(436784329.828) == sig_fig(436784329.828746, 12), "Rounding to 12 sig fig failed."
        assert Decimal(436784329.82) == sig_fig(436784329.828746, 11), "Rounding to 11 sig fig failed."
        assert Decimal(436784329.8) == sig_fig(436784329.828746, 10), "Rounding to 10 sig fig failed."
        assert Decimal(436784329) == sig_fig(436784329.828746, 9), "Rounding to 9 sig fig failed."
        assert Decimal(436784320) == sig_fig(436784329.828746, 8), "Rounding to 8 sig fig failed."
        assert Decimal(436784300) == sig_fig(436784329.828746, 7), "Rounding to 7 sig fig failed."
        assert Decimal(436784000) == sig_fig(436784329.828746, 6), "Rounding to 6 sig fig failed."
        assert Decimal(436780000) == sig_fig(436784329.828746, 5), "Rounding to 5 sig fig failed."
        assert Decimal(436700000) == sig_fig(436784329.828746, 4), "Rounding to 4 sig fig failed."
        assert Decimal(436000000) == sig_fig(436784329.828746, 3), "Rounding to 3 sig fig failed."
        assert Decimal(430000000) == sig_fig(436784329.828746, 2), "Rounding to 2 sig fig failed."
        assert Decimal(400000000) == sig_fig(436784329.828746, 1), "Rounding to 1 sig fig failed."

    def test_standardForm(self):
        pass#TODO:

    def test_trueRound(self):
        pass#TODO:

    def test_consistancyTest(self):
        pass#TODO:

    def test_GraphAndErrorString(self):
        x = np.array([1.3, 2.1, 2.8, 3.9, 5.2])
        y = np.array([3.4, 4.6, 7.2, 8.5, 11.2])

        dx = np.array([1, 1, 1, 1, 1])
        dy = np.array([1, 1, 1, 1, 1])

        testGraph = Figure(x, y, dx, dy, size = None, title = "A test graph", xLabel = "X-Axis", yLabel = "Y-Axis", saveName = "testingFigure.png")
        testGraph.createFitLine()
        testGraph.plot()
        testGraph.save()
        #testGraph.show()# TODO: window hangs

        m = testGraph.fit.fitVariables["m"]
        c = testGraph.fit.fitVariables["c"]

        assert "2.0435922040733323" == str(m[0]), "The value calculated for the gradient does not match the expected value."
        assert "0.7481821730455976" == str(m[1]), "The error calculated for the gradient does not match the expected value."
        assert "0.7266078556762237" == str(c[0]), "The value calculated for the intercept does not match the expected value."
        assert "2.505349774682801" == str(c[1]), "The error calculated for the intercept does not match the expected value."

        assert "2.0435922040733323 \u00B1 0.7" == error_string(m[0], m[1]), "The normalised value and error calculated for the gradient does not match the expected value."
        assert "0.7266078556762237 \u00B1 3.0" == error_string(c[0], c[1]), "The normalised value and error calculated for the intercept does not match the expected value."
