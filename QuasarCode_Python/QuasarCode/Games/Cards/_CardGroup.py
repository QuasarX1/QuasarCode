from random import Random
from QuasarCode.Games.Cards import IPlayingCard

class CardGroup(list):
    """
    A list of IPlayingCards. Can be used as an ordenary Python list.

    Atributes:
        str Name --> name of the collection

    __init__():
        str name --> name of the collection
        list cards --> list of IPlayingCards to initialise the collection with (deafult is blank list)
    """
    def __init__(self, name: str, cards: list = []):
        self.Name = name
        self += cards

    def Remove(self, index: int) -> IPlayingCard:
        """
        Remove a card from the collection at the specified index
        """
        element = self[index]
        del self[index]
        return element

    def Shuffle(self):
        """
        Randomises the order of the cards in the group
        """
        generator = Random()
        newOrder = []

        while len(self) > 0:
            position = generator.randint(0, len(self) - 1)
            newOrder.append(self.Remove(position))

        self += newOrder

    def ReturnCards(self, sender: object):
        """
        Event handler for requesting the return of cards
        """
        self.clear()

    def __str__(self):
        return self.Name + ": " + super().__str__()

    def sort(self, *args, **kwargs):
        if "key" in kwargs.keys():
            return super().sort(*args, **kwargs)
        else:
            return super().sort(*args, key = lambda card: (card.Value + 1) * (card.Suit + 1), **kwargs)