from QuasarCode.Games.Cards import CardGroup

class Deck(CardGroup):
    """
    """
    def __init__(self, name: str, jokers: int = 0):
        self.Jokers: int = jokers

        self.Cards: list = []#

        self.super().__init__(name, self.Cards)