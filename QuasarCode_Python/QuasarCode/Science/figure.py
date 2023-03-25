import numpy as np
from matplotlib import pyplot as plt
from .fitline import LineOfBestFit, LineType

class DrawInstruction(object):
    """
    A data type for storing an instruction to draw a single item on a ManualFigure object.

    Arguments:
        deligate function -> A function with signiture (axis, *args, **kwargs) that edits the axis.
        list draw_args -> A list containing the function arguments.
        dict draw_kwargs -> A dictionary containing named function arguments.
    """

    def __init__(self, function, draw_args, draw_kwargs):
        self.__function = function
        self.__function_args = draw_args
        self.__function_kwargs = draw_kwargs

    def run(self, axis):
        """
        Executes the instruction an a provided axis.
        """
        self.__function(axis, *self.__function_args, **self.__function_kwargs)

    @staticmethod
    def plot(axis, *args, **kwargs):
        """
        Provided wrapper for the pyplot draw method.
        """
        axis.plot(*args, **kwargs)

    @staticmethod
    def errorbar(axis, *args, **kwargs):
        """
        Provided wrapper for the pyplot errorbar method.
        """
        axis.errorbar(*args, **kwargs)

    @staticmethod
    def scatter(axis, *args, **kwargs):
        """
        Provided wrapper for the pyplot scatter method.
        """
        axis.scatter(*args, **kwargs)

class IAutomaticFigure(object):
    """
    Interface for the Figure object.
    Any object that inherits this and defines "x", "y", "xError" and "yError" members
    that are publicly avalable will be treated as a valid object for use with the LineOfBestFit constructor.
    """

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_xError(self):
        return self.xError
    def get_yError(self):
        return self.yError

class ManualFigure(object):
    """
    A figure compatable with the QuasarCode.Science.Graph object that allows
    for a similar implementation of figures to the native matplotlib.pyplot one.
    Some added functionality has been made avalable.

    Arguments:
        tuple size -> A tuple with the horizontal and vertical size of the figure. (Defult is (6.4, 4.8))

        string title -> The title to be displayed on the graph. (Default is "")

        string xLabel -> The axis label to be displayed on the x-axis. (Default is "")

        string yLabel -> The axis label to be displayed on the y-axis. (Default is "")

        string saveName -> The png file name (can be precided with a file path) to save the graph under. (Default is "figure.png")
    """

    def __init__(self, size = None, title = "", xLabel = "", yLabel = "", saveName = "figure.png"):
        self.figure = plt.figure()
        self.size = size if size is not None else (6.4, 4.8)# This is the deafult as documented by https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html
        self.axis = None
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.saveName = saveName

        self.instructions = []

        self.plot()

    def plot(self, axisOveride = None):
        """
        Draws all the instructions on an axis.

        Arguments:
            matplotlib.axes._subplots.AxesSubplot axisOveride -> an alternitive axis to draw on.
        """
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
        """
        Saves the figure in its current state as a png using the current save name.

        Arguments:
            string nameOveride -> The filename or filepath to use instead of the one stored by the object.
        """
        if nameOveride is not None and nameOveride != "":
            self.figure.savefig(nameOveride)
        elif self.saveName is not None and self.saveName != "":
            self.figure.savefig(self.saveName)

    def show(self):
        """
        Show the figure in a window.
        """
        self.figure.show()

    def addInstruction(self, function, *args, **kwargs):
        """
        Adds an instruction to the figure.
        This will be executed when the plot method is called.

        Arguments:
            deligate function -> the function to be executed that will edit the axis object.
                                See the static members of the DrawInstruction class for
                                some pre existing ones ready for use.

            Other arguments will be passed to the function specified.

            Other named arguments will be passed to the function specified.
        """
        self.instructions.append(DrawInstruction(function, args, kwargs))

    def clearInstructions(self):
        """
        Removes all the instructions.
        """
        self.instructions = []

    def addFit(self, x, y, xError = None, yError = None, lineType: LineType = LineType.straight, initialFitVariables: dict = None, customFitMethods: list = None, **kwargs):
        """
        Adds an instruction to draw a fit line using the data provided.

        Arguments:
            numpy.ndarray x -> The x coortinates of the data points.

            numpy.ndarray y -> The y coortinates of the data points.

            numpy.ndarray xError -> The errors on the x coordinates. Used to produce a horisontal errorbar.

            numpy.ndarray yError -> The errors on the y coordinates. Used to produce a vertical errorbar.
            
            LineType type -> The type of fit to plot. Options are from the LineType enum.

            dict initialFitVariables -> A dictionary containing the fit variables and their starting value used to
                                    overide he defults or to specify a custom fit. Variables should be in oposite
                                    order to that expected by the fitting functions i.e. m then c for y = m * x + c (Defult is None)

            list customFitMethods -> A list with two items: [the fitting function, the error function] (Defult is None)

            All other named arguments will be passed to the plot function used to draw the line.
        """
        if xError is not None:
            xError = np.array(xError)
        if yError is not None:
            yError = np.array(yError)
        fit = LineOfBestFit(ManualFigure.__FigureSpoofer(np.array(x), np.array(y), xError, yError), lineType, initialFitVariables, customFitMethods)

        if fit.fit_Y is not None:
            self.addInstruction(DrawInstruction.plot, [fit.fit_X, fit.fit_Y], *kwargs)

    class __FigureSpoofer(IAutomaticFigure):
        """
        A class that acts as a Figure object so the LineOfBestFit object can be created.
        """

        def __init__(self, x, y, dx, dy):
            self.x = x
            self.y = y
            self.xError = dx
            self.yError = dy

class Figure(IAutomaticFigure):
    """
    A figure object for encapsulating a matplotlib.pyplot graph working with a set of data and
    displaying it along with multiple optional lines of best fit.
    Automaticly formats the figure produced and allows overiding of all the usual pyplot features.

    Arguments:
        numpy.ndarray x -> The x coortinates of the data points.

        numpy.ndarray y -> The y coortinates of the data points.

        numpy.ndarray xError -> The errors on the x coordinates. Used to produce a horisontal errorbar.

        numpy.ndarray yError -> The errors on the y coordinates. Used to produce a vertical errorbar.

        tuple size -> A tuple with the horizontal and vertical size of the figure. (Defult is (6.4, 4.8))

        LineType fitLine -> The type of fit to plot. Options are from the LineType enum.
                            LineType.custom isn't valid - specify as None or as
                            LineType.none and then create the custom line seperately. (Defult is None)

        string title -> The title to be displayed on the graph. (Default is "")

        string xLabel -> The axis label to be displayed on the x-axis. (Default is "")

        string yLabel -> The axis label to be displayed on the y-axis. (Default is "")

        string saveName -> The png file name (can be precided with a file path) to save the graph under. (Default is "figure.png")
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
        """
        Draws the figure onto an axis.

        Arguments:
            matplotlib.axes._subplots.AxesSubplot axisOveride -> an alternitive axis to draw on.

            All named arguments will be passed on to the plotting method of the axis (axis.plot or axis.errorbar).
        """
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
            self.axis.errorbar(self.x, self.y, self.yError, self.xError, **self.__dataPlotKwargs)

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
        """
        Creates a new line of best fit using the figure's data.

        Arguments:
            LineType type -> The type of fit to plot. Options are from the LineType enum.

            bool clearOthers -> Wether or not to clear all of the other lines of best fit. (Default is True)

            dict initialFitVariables -> A dictionary containing the fit variables and their starting value used to
                                    overide he defults or to specify a custom fit. Variables should be in oposite
                                    order to that expected by the fitting functions i.e. m then c for y = m * x + c (Defult is None)

            list customFitMethods -> A list with two items: [the fitting function, the error function] (Defult is None)

            All other named arguments will be passed to the plot function used to draw the line.
        """
        if clearOthers:
            self.fitLines = []
            self.__fitLineKwargs = []
        
        if type is not None:
            self.fitLines.append(LineOfBestFit(self, type, initialFitVariables, customFitMethods))
            self.__fitLineKwargs.append(kwargs)

    def save(self, nameOveride = None):
        """
        Saves the figure in its current state as a png using the current save name.

        Arguments:
            string nameOveride -> The filename or filepath to use instead of the one stored by the object.
        """
        if nameOveride is not None and nameOveride != "":
            self.figure.savefig(nameOveride)
        elif self.saveName is not None and self.saveName != "":
            self.figure.savefig(self.saveName)

    def show(self):
        """
        Show the figure in a window.
        """
        self.figure.show()


    # Property Accessors
    
    def setXRange(self, value: tuple):
        """
        Sets the range ov values on the x-axis
        """
        self.customXRange = True
        self.__xRange = value

    def setYRange(self, value: tuple):
        """
        Sets the range ov values on the y-axis
        """
        self.customYRange = True
        self.__yRange = value

    def getFittingOutput(self):
        """
        Retrives the output form all of the lines of best fit.
        """
        return "\n--------\n".join([fit.fittingOutput for fit in self.fitLines])