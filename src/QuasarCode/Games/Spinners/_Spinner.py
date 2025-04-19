from ._ISpinner import ISpinner
import random

class Spinner(ISpinner):
    """
    Creates spinner objects with n sides and labels. Labels are selected and returned by calling the avalable methods.

    __init__():
        list labels --> list of labels - one for each side
        int seed --> seed for the random generator (deafult is None)
    """
    def __init__(self, labels: list, seed: int = None):
        self.__Generator: random.Random = random.Random() if seed == None else random.Random(seed)
        self.Labels: list = list(labels)
        self.Sides: int = len(labels)

    def ContextSpin(self):
        """
        Randomly selects a side and retuns the side and the corisponding label.
        """
        index = self.__Generator.randint(0, self.Sides)
        return (index, self.Labels[index])

    def Spin(self):
        """
        Randomly selects a side and retuns the corisponding label.
        """
        return self.Labels[self.__Generator.randint(0, self.Sides)]
        
    def IndexSpin(self):
        """
        Randomly selects a side and retuns the side number.
        """
        return self.__Generator.randint(0, self.Sides)