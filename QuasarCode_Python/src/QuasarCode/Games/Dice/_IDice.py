class IDice(object):
    """
    A dice that can be rolled to produce an integer result starting from 1
    """
    @property
    def Sides(self) -> int:
        """
        Number of sides on the dice
        """
        raise NotImplementedError()

    def Roll(self):
        """
        Rolls the dice
        """
        raise NotImplementedError()