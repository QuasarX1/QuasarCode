import numpy as np
from matplotlib import pyplot as plt
from QuasarCode.Science.figure import Figure

class Graph(object):
    """
    Displays multiple figures as a single figure and allows them to be saved as a single figure.

    Arguments:
        list[Figure] figures -> A list of figures to display in order. Must have at least one item if the "data" paramiter is blank. (Default is [])

        list[list] data -> A list of lists of paramiters to be passed to the Figure object constructor. Must have at least one item if the "figures" paramiter is blank. (Default is [])

        tuple shape -> The number of columns and rows to use to display the individual figures. (Default is (1, 1))

        tuple size -> A tuple with the horizontal and vertical size of each individual figure. (Defult is (6.4, 4.8))

        string title -> The title to be displayed on the graph. (Default is "")

        string saveName -> The png file name (can be precided with a file path) to save the graph under. (Default is "figure.png")
    """

    def __init__(self, figures = [], data = [], shape = (1, 1), size = None, title = "", saveName = "figure.png"):
        self.title = title
        self.saveName = saveName
        self.size = size if size is not None else [6.4, 4.8]# This is the deafult as documented by https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html

        self.__shape = shape if len(shape) > 1 else (shape[0], 1)
        self.figure, self.axes = plt.subplots(ncols = self.__shape[0], nrows = self.__shape[1])
        if not isinstance(self.axes, np.ndarray):
            self.axes = [[self.axes]]
        elif not isinstance(self.axes[0], np.ndarray):
            self.axes = [self.axes]

        self.figures = figures

        self.data = np.array(data)

        # The number of extra figures needed to hold the data provided
        requiredFigures = np.shape(self.data)[0]#TODO: make this a more robust check

        if requiredFigures + len(self.figures) > self.__shape[0] * self.__shape[1]:
            raise ValueError("The shape provided didn't allow enough space for all of the figures provided. The shape allowed for {} but {} were avalable.".format(shape[0] * (shape[1] if len(shape) > 1 else 1), requiredFigures + len(self.figures)))

        # Adds the extra figures
        for i in range(requiredFigures):
            self.figures.append(Figure(*self.data[i]))

        self.numberOfFigures = len(self.figures)

        self.plot()

    def plot(self, options = None):
        """
        Draws the figure onto an axis.

        Arguments:
            matplotlib.axes._subplots.AxesSubplot axisOveride -> an alternitive axis to draw on.

            dict options -> Named arguments to be passed to all the plot methods of the contained figure objects.
                            Argument names should be strings. (Default is None)

            OR

            list[dict] options -> A list of dicts - one for each figure for the same purpose as the above. (Default is None)
        """
        for i in range(self.numberOfFigures):
            axis = self.axes[i // self.__shape[0]][i - (i // self.__shape[1]) * self.__shape[0]]
            axis.cla()
            self.figures[i].plot(axis, **(options if isinstance(options, dict) else (options[i] if isinstance(options, list) and len(options) > i and isinstance(options[i], dict) else {}) ))

        self.figure.set_figwidth(self.size[0])
        self.figure.set_figheight(self.size[1])
            
    def save(self, nameOveride = None):
        """
        Saves the graph in its current state as a png using the current save name.

        Arguments:
            string nameOveride -> The filename or filepath to use instead of the one stored by the object.
        """
        if nameOveride is not None and nameOveride != "":
            self.figure.savefig(nameOveride)
        elif self.saveName is not None and self.saveName != "":
            self.figure.savefig(self.saveName)

    def show(self):
        """
        Show the figure(s) in a window.
        """
        self.figure.show()