import numpy as np
from matplotlib import pyplot as plt
from QuasarCode.Science.figure import Figure

class Graph(object):
    """
    """

    def __init__(self, figures = [], data = [], shape = (1, 1), size = None, title = "", saveName = "figure.png", axisAlocationOveride = {}):
        self.title = title
        self.saveName = saveName
        self.size = figsize = size if size is not None else [6.4, 4.8]# This is the deafult as documented by https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html

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
        options as dict to apply to all or as list of dict to apply to in order
        """
        for i in range(self.numberOfFigures):
            axis = self.axes[i // self.__shape[0]][i - (i // self.__shape[1]) * self.__shape[0]]
            axis.cla()
            self.figures[i].plot(axis, **(options if isinstance(options, dict) else (options[i] if isinstance(options, list) and len(options) > i and isinstance(options[i], dict) else {}) ))

        self.figure.set_figwidth(self.size[0])
        self.figure.set_figheight(self.size[1])
            
    def save(self, nameOveride = None):
        if nameOveride is not None and nameOveride != "":
            self.figure.savefig(nameOveride)
        elif self.saveName is not None and self.saveName != "":
            self.figure.savefig(self.saveName)

    def show(self):
        self.figure.show()