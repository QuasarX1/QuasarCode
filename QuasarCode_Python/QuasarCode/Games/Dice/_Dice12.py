from QuasarCode.Games.Dice import NDice

class Dice12(NDice):
    """
    Simple dice with 12 sides

    __init__():
        int seed --> seed for the random generator (deafult is None)
    """
    def __init__(self, seed = None):
        super.__init__(12, seed)