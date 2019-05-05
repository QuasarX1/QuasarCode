from QuasarCode.Games.Dice import IDice
import random

class NDice(IDice):
    """
    A dice with a specified number of sides

    __init__():
        int sides --> number of sides on the dice
        int seed --> seed for the random generator (deafult is None)
    """
    def __init__(self, sides: int, seed: int = None):
        self.__Generator: random.Random = random.Random() if seed == None else random.Random(seed)

        # Number of sides on the dice
        self.Sides: int

    def Roll(self):
        """
        Rolls the dice
        """
        return self.__Generator.randint(1, self.Sides + 1)

    def MultipleDice(sides: list, noOfDice: int = len(sides)):
        """
        Convenience method for creating multiple dice

        Paramiters:
            list sides --> list of side numbers representing unique dice. For multiple of the same number, use a single element and alter noOfDice
            int noOfDice --> number of dice to create (deafult is length of sides list)
        """
        if len(sides) > 1:
            randomiser = random.Random()
            return [NDice(size, randomiser.Next(100000, 999999)) for size in sides]

        else:
            randomiser = random.Random()
            return [NDice(sides[0], randomiser.Next(100000, 999999)) for i in noOfDice]