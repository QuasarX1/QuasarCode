class UndersubscribedEventError(BaseException):
    """
    Indicates that there are two few subscribers to perform the requested operation.
    """
    def __init__(self, message):
        self.message = message