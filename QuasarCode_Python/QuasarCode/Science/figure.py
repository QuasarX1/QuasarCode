import numpy as np
from matplotlib import pyplot as plt
from QuasarCode.Science.fitline import LineOfBestFit, LineType

class DrawInstruction(object):
    def __init__(self, function, draw_args, draw_kwargs):
        self.__function = function
        self.__function_args = draw_args
        self.__function_kwargs = draw_kwargs

    def run(self, axis):
        self.__function(axis, *self.__function_args, **self.__function_kwargs)

    @staticmethod
    def plot(axis, *args, **kwargs):
        axis.plot(*args, **kwargs)

    @staticmethod
    def errorbar(axis, *args, **kwargs):
        axis.errorbar(*args, **kwargs)

    @staticmethod
    def scatter(axis, *args, **kwargs):
        axis.scatter(*args, **kwargs)

class ManualFigure(object):
    """
    """
    def __init__(self, size = None, title = "", xLabel = "", yLabel = "", saveName = "figure.png"):
        self.figure = plt.figure()
        self.size = size if size is not None else [6.4, 4.8]# This is the deafult as documented by https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html
        self.axis = None
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.saveName = saveName

        self.instructions = []

        self.plot()

    def plot(self, axisOveride = None):
        if axisOveride is None:
            self.figure.clf()
            self.axis = self.figure.gca()
        else:
            self.axis = axisOveride

        for instruction in self.instructions:
            instruction.run(self.axis)

        self.axis.set_title(self.title)
        self.axis.set_xlabel(self.xLabel)
        self.axis.set_ylabel(self.yLabel)

        self.figure.set_figwidth(self.size[0])
        self.figure.set_figheight(self.size[1])

    def save(self, nameOveride = None):
        if nameOveride is not None and nameOveride != "":
            self.figure.savefig(nameOveride)
        elif self.saveName is not None and self.saveName != "":
            self.figure.savefig(self.saveName)

    def show(self):
        self.figure.show()

    def addInstruction(self, function, *args, **kwargs):
        self.instructions.append(DrawInstruction(function, args, kwargs))

    def clearInstructions(self):
        self.instructions = []

class Figure(object):
    """
    """

    def __init__(self, x, y, xError = None, yError = None, size = None, fitLine = None, title = "", xLabel = "", yLabel = "", saveName = "figure.png"):
        self.figure = plt.figure(figsize = size)
        self.size = size if size is not None else [6.4, 4.8]# This is the deafult as documented by https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html
        self.axis = None
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.saveName = saveName

        self.__fitLineKwargs = []
        self.__dataPlotKwargs = []

        self.x: np.ndarray = np.array(x)
        self.y: np.ndarray = np.array(y)

        self.xError: np.ndarray = np.array(xError) if xError is not None else None
        self.yError: np.ndarray = np.array(yError) if yError is not None else None

        self.showErrorBars = True
        self.fitLines = []

        self.customXRange = False
        self.__xRange = (None, None)
        self.xRange = property(fget = (lambda self: self.__xRange), fset = self.setXRange)
        
        self.customYRange = False
        self.__yRange = (None, None)
        self.yRange = property(fget = lambda self: self.__yRange, fset = self.setYRange)

        if isinstance(fitLine, LineType) and fitLine != LineType.none and fitLine is not None:
            self.createFitLine(type = fitLine)

        self.plot()

    def plot(self, axisOveride = None, **kwargs):
        self.__dataPlotKwargs = kwargs

        if axisOveride is None:
            self.figure.clf()
            self.axis = self.figure.gca()
        else:
            self.axis = axisOveride

        if self.showErrorBars and (self.xError is not None or self.yError is not None):
            # Add deafult styling to the kwargs if not allready present
            if "fmt" not in self.__dataPlotKwargs:
                self.__dataPlotKwargs["fmt"] = "r"
            if "linestyle" not in self.__dataPlotKwargs:
                self.__dataPlotKwargs["linestyle"] = ""

            # Plot the data with avalable errorbars
            self.axis.errorbar(self.x, self.y, self.xError, self.yError, **self.__dataPlotKwargs)

            # Ajust the x range
            if not self.customXRange:
                errorAjustX = [0, 0]
                if self.xError is not None:
                    errorAjustX[0] = self.xError[np.asarray(self.x == min(self.x)).nonzero()[0]]
                    errorAjustX[1] = self.xError[np.asarray(self.x == max(self.x)).nonzero()[0]]

                self.__xRange = (min(self.x) - errorAjustX[0], max(self.x) + errorAjustX[1])

            # Ajust the y range
            if not self.customYRange:
                errorAjustY = [0, 0]
                if self.yError is not None:
                    errorAjustY[0] = self.yError[np.asarray(self.y == min(self.y)).nonzero()[0]]
                    errorAjustY[1] = self.yError[np.asarray(self.y == max(self.y)).nonzero()[0]]

                self.__yRange = (min(self.y) - errorAjustY[0], max(self.y) + errorAjustY[1])

        else:
            # Plot the data
            self.axis.scatter(self.x, self.y, **self.__dataPlotKwargs)

            if not self.customXRange:
                self.__xRange = (min(self.x), max(self.x))
            if not self.customYRange:
                self.__yRange = (min(self.y), max(self.y))

        self.axis.set_xlim([self.__xRange[0], self.__xRange[1]])
        self.axis.set_ylim([self.__yRange[0], self.__yRange[1]])

        for i, line in enumerate(self.fitLines):
            if line.fit_Y is not None:
                self.axis.plot(line.fit_X, line.fit_Y, **self.__fitLineKwargs[i])

        self.axis.set_title(self.title)
        self.axis.set_xlabel(self.xLabel)
        self.axis.set_ylabel(self.yLabel)

        self.figure.set_figwidth(self.size[0])
        self.figure.set_figheight(self.size[1])

    def createFitLine(self, type: LineType = LineType.straight, clearOthers = True, initialFitVariables: dict = None, customFitMethods: list = None, **kwargs):
        if clearOthers:
            self.fitLines = []
            self.__fitLineKwargs = []
        
        if type is not None:
            self.fitLines.append(LineOfBestFit(type, self, initialFitVariables, customFitMethods))
            self.__fitLineKwargs.append(kwargs)

    def save(self, nameOveride = None):
        if nameOveride is not None and nameOveride != "":
            self.figure.savefig(nameOveride)
        elif self.saveName is not None and self.saveName != "":
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

    def getFittingOutput(self):
        return "\n--------\n".join([fit.fittingOutput for fit in self.fitLines])