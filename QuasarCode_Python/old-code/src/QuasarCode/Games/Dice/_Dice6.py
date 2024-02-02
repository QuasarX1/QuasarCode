from ._NDice import NDice

class Dice6(NDice):
    """
    Simple dice with 6 sides

    __init__():
        int seed --> seed for the random generator (deafult is None)
    """
    def __init__(self, seed = None):
        super.__init__(6, seed)