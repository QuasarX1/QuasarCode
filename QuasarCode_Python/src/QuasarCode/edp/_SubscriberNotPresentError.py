class SubscriberNotPresentError(BaseException):
    """
    Indicates that a specific subscriber is not listed as a subscriber to the event.
    """
    def __init__(self, message):
        self.message = message