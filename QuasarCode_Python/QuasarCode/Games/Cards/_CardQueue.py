from QuasarCode.Games.Cards import CardGroup, IPlayingCard

class CardQueue(CardGroup):
    """
    A CardGroup queue data structure containing IPlayingCards

    NOTE: This is only a convenience structure that mirrors the CardQueue from the C# library.
            The CardGroup can be used like a queue in the same way as a Python list.

    Atributes:
        str Name --> name of the collection

    __init__():
        str name --> name of the collection
        list cards --> list of IPlayingCards to initialise the collection with (deafult is blank list)
    """
    def __init__(self, name: str, cards: list = []):
        super().__init__(name, cards)

    def Push(self, item: IPlayingCard):
        self.append(item)

    def Pop(self) -> IPlayingCard:
        return self.pop(0)