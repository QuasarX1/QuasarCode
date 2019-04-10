from enum import Enum

class LineType(Enum):
    straight = 0

class LineOfBestFit(object):
    """
    """

    def __init__(self, lineType: LineType = LineType.straight, graph = None):
        self.lineType = lineType
        self.graph = graph

        self.fittingOutput = None
        self.fit = None

        self.runFit()

    def runFit(self):
        """
        """
        if self.lineType == LineType.straight:
            pass