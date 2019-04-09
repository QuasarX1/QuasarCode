import numpy as np
from matplotlib import pyplot as plt
import fitline

class Figure(object):
    """
    """

    def __init__(self, x, y, xError, yError, size = None, title = "", xLabel = "", yLabel = "", saveName = "figure.png"):
        self.figure = plt.figure(figsize = size if size is not None else None)

        self.x: np.ndarray = np.array(x)
        self.y: np.ndarray = np.array(y)

        self.xError: np.ndarray = np.array(xError)
        self.yError: np.ndarray = np.array(yError)

        self.showErrorBars = True
        self.fit = None

        self.customXRange = False
        self.__xRange = (None, None)
        self.xRange = property(fget = (lambda self: self.__xRange), fset = setXRange)
        
        self.customYRange = False
        self.__yRange = (None, None)
        self.yRange = property(fget = lambda self: self.__yRange, fset = setYRange)

        self.plot()

    def plot(self):
        if self.showErrorBars and (self.xError is not None or self.yError is not None):
            self.figure.errorbar(self.x, self.y, self.xError, self.yError)

            if not self.customXRange:
                self.xRange = (min(self.x) - self.xError[self.xError.index(min(self.x))], max(self.x) + self.xError[self.xError.index(max(self.x))])
            if not self.customYRange:
                self.yRange = (min(self.x) - self.yError[self.yError.index(min(self.y))], max(self.y) + self.yError[self.yError.index(max(self.y))])
        else:
            self.figure.scatter(self.x, self.y)

            if not self.customXRange:
                self.xRange = (min(self.x), max(self.x))
            if not self.customYRange:
                self.yRange = (min(self.x), max(self.y))

        self.figure.xRange(self.__xRange[0], self.__xRange[1])
        self.figure.yRange(self.__yRange[0], self.__yRange[1])

        if self.fit is not None:
            self.figure.plot(self.x, self.fit.fit)

    def createFitLine(self, type: fitline.LineOfBestFit.LineType = fitline.LineOfBestFit.LineType.straight):
        self.fit = fitline.LineOfBestFit(type, self)

    def show():
        self.figure.show()


    # Property Accessors

    def setXRange(self, value):
        self.customXRange = True; __xRange = value

    def setYRange(self, value):
        self.customYRange = True; __yRange = value