class ISpinner(object):
    """
    Interface for all Spinner objects.
    """

    @property
    def Labels(self) -> list:
        """
        Array of side labels
        """
        raise NotImplementedError()

    @property
    def Sides(self) -> int:
        """
        Number of sides/labels
        """
        raise NotImplementedError()

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