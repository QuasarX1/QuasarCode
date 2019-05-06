class IPlayingCard(object):

    @property
    def Value(self):
        raise NotImplementedError()

    @property
    def Suit(self):
        raise NotImplementedError()