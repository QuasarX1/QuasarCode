class IPlayingCard(object):

    @property
    def Value(self) -> int:
        raise NotImplementedError()

    @property
    def Suit(self) -> int:#TODO: change for card suit
        raise NotImplementedError()