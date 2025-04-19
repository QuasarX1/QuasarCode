class NotEnoughArgumentsError(BaseException):
    """
    Indicates that not enough arguments were passed for the function signiture of a subscribed method during event running.
    """
    def __init__(self, message):
        self.message = message