from enum import Enum

class LineOfBestFit(object):
    """
    """

    def __init__(self, lineType: LineTypes = LineType.straight, graph = None):
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

    class LineType(Enum):
        straight