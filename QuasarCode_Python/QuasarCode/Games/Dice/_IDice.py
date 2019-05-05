class IDice(object):
    """
    A dice that can be rolled to produce an integer result starting from 1
    """
    def __init__(self):
        # Number of sides on the dice
        self.Sides: int

    def Roll(self):
        """
        Rolls the dice
        """
        raise NotImplementedError()