import numpy as np
from matplotlib import pyplot as plt
from QuasarCode.Science.fitline import LineOfBestFit, LineType

class Figure(object):
    """
    """

    def __init__(self, x, y, xError, yError, size = None, title = "", xLabel = "", yLabel = "", saveName = "figure.png"):
        self.figure = plt.figure(figsize = size if size is not None else None)
        self.axis = None
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.saveName = saveName

        self.x: np.ndarray = np.array(x)
        self.y: np.ndarray = np.array(y)

        self.xError: np.ndarray = np.array(xError)
        self.yError: np.ndarray = np.array(yError)

        self.showErrorBars = True
        self.fit = None

        self.customXRange = False
        self.__xRange = (None, None)
        self.xRange = property(fget = (lambda self: self.__xRange), fset = self.setXRange)
        
        self.customYRange = False
        self.__yRange = (None, None)
        self.yRange = property(fget = lambda self: self.__yRange, fset = self.setYRange)

        self.plot()

    def plot(self):
        self.figure.clf()
        self.axis = self.figure.gca()

        if self.showErrorBars and (self.xError is not None or self.yError is not None):
            self.axis.errorbar(self.x, self.y, self.xError, self.yError, fmt='r', linestyle = '')

            if not self.customXRange:# TODO: alter indexing of retrived indeces
                #self.xRange = (min(self.x) - self.xError[self.x.index(min(self.x))], max(self.x) + self.xError[self.x.index(max(self.x))])
                self.xRange = (min(self.x) - self.xError[np.asarray(self.x == min(self.x)).nonzero()[0]], max(self.x) + self.xError[np.asarray(self.x == max(self.x)).nonzero()[0]])
            if not self.customYRange:
                self.yRange = (min(self.y) - self.yError[np.asarray(self.y == min(self.y)).nonzero()[0]], max(self.y) + self.yError[np.asarray(self.y == max(self.y)).nonzero()[0]])
        else:
            self.axis.scatter(self.x, self.y)

            if not self.customXRange:
                self.xRange = (min(self.x), max(self.x))
            if not self.customYRange:
                self.yRange = (min(self.x), max(self.y))

        self.axis.set_xlim([self.__xRange[0], self.__xRange[1]])
        self.axis.set_ylim([self.__yRange[0], self.__yRange[1]])

        if self.fit is not None:
            self.axis.plot(self.x, self.fit.fit)

    def createFitLine(self, type: LineType = LineType.straight):
        self.fit = LineOfBestFit(type, self)

    def save(self):
        if self.saveName is not None and self.saveName != "":
            self.figure.savefig(self.saveName)

    def show(self):
        self.figure.show()


    # Property Accessors

    def setXRange(self, value):
        self.customXRange = True
        self.__xRange = value

    def setYRange(self, value):
        self.customYRange = True
        self.__yRange = value