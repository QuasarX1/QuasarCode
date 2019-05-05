class ISpinner(object):
    """
    Interface for all Spinner objects.
    """
    def __init__(self):
        # Array of side labels
        self.Labels: list

        # Number of sides/labels
        self.Sides: int

    def ContextSpin(self):
        """
        Randomly selects a side and retuns the side and the corisponding label.
        """
        raise NotImplementedError()

    def Spin(self):
        """
        Randomly selects a side and retuns the corisponding label.
        """
        raise NotImplementedError()

    def IndexSpin(self):
        """
        Randomly selects a side and retuns the side number.
        """
        raise NotImplementedError()