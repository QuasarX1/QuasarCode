from QuasarCode.Games.Cards import PlayingCard

class IPlayingCard(object):
    """
    A card from a standard deck of 52 playing cards
    """

    @property
    def Value(self) -> PlayingCard.AllowedValues:
        """
        The card's value
        """
        raise NotImplementedError()

    @property
    def Suit(self) -> PlayingCard.AllowedSuits:
        """
        The card's suit
        """
        raise NotImplementedError()