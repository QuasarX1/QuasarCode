from collections.abc import MutableSequence
from ._NDice import NDice

class DiceCup(MutableSequence):
    """
    Collection of NDice objects that are rolled together

    Atributes:
        list AllDice --> list of the NDice objects rolled by the cup
        int Count --> number of dice stored
        bool Dynamic --> whether or not the cup is mutable

    __init__():
        list sides --> list of side numbers representing unique dice. For multiple of the same number, use a single element and alter noOfDice
        int noOfDice --> number of dice to create (deafult is length of sides list)
        bool dynamic --> whether or not the cup is mutable
    """
    def __init__(self, sides: list, noOfDice: int = None, dynamic: bool = False):
        #? super().__init__()

        self.Dynamic = dynamic
        self.AllDice: list = NDice.MultipleDice(sides, noOfDice)

        self.Count: int = property(fget = lambda self: len(self.AllDice))

        if not dynamic and len(self.AllDice) == 0:
            raise ValueError("No dice were specified for a static dice cup.")

    def Roll(self, suppressEmptyExeption = False):
        """
        Rolls all the dice and returns each individual result
        """
        if not suppressEmptyExeption and self.Count == 0:
            raise ValueError("There are no dice in the cup.");

        results = []

        for dice in self.AllDice:
            results.append(dice.Roll())

        return results

    def RollTotal(self, suppressEmptyExeption = False):
        """
        Rolls all the dice and returns the sum of the results
        """
        return sum(self.Roll(suppressEmptyExeption))

    def __getitem__(self, key):
        if not self.Dynamic:
            raise RuntimeError("Invalid operation - the dice cup is not dynamic!")

        return self.AllDice.__getitem__(key)

    def __setitem__(self, key, value):
        if not self.Dynamic:
            raise RuntimeError("Invalid operation - the dice cup is not dynamic!")

        self.AllDice.__setitem__(key, value)

    def __delitem__(self, key):
        if not self.Dynamic:
            raise RuntimeError("Invalid operation - the dice cup is not dynamic!")

        self.AllDice.__delitem__(key)

    def __len__(self):
        return len(self.AllDice)

    def insert(self, index, object):
        if not self.Dynamic:
            raise RuntimeError("Invalid operation - the dice cup is not dynamic!")

        self.AllDice.insert(index, object)

    def __iadd__(self, value):
        self.append(value)
        return self