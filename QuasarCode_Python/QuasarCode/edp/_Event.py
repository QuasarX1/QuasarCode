from QuasarCode.edp._UndersubscribedEventError import UndersubscribedEventError
from QuasarCode.edp._SubscriberNotPresentError import SubscriberNotPresentError
from QuasarCode.edp._NotEnoughArgumentsError import NotEnoughArgumentsError

class Event(object):
    """
    Implements Event Driven programming in Python (edp)
    """

    def __init__(self):
        self.__subscribers = []
    
    def subscribe(self, func):
        """
        Registers a method with the event instance
        For syntactic sugar, use event += func
        """
        self.__subscribers.append(func)
    
    def __iadd__(self, func):
        """
        Registers a method with the event instance
        Sintactic sugar for Event.subscribe(func)
        """
        self.subscribe(func)
        return self
    
    def unsubscribe(self, func):
        """
        Removes the registration of a method from the event instance
        For syntactic sugar, use event -= func
        """
        if len(self.__subscribers) == 0:
            raise UndersubscribedEventError("No subscribers.")
        try:
            self.__subscribers.remove(func)
        except ValueError:
            raise SubscriberNotPresentError("The provided subscriber was not listed as a subscriber to the event.")
    
    def __isub__(self, func):
        """
        Removes the registration of a method from the event instance
        Sintactic sugar for Event.unsubscribe(func)
        """
        self.unsubscribe(func)
        return self
    
    def run(self, *args, **kwargs):
        """
        Calls the event passing any *args and **kwargs accross
        """
        if len(self.__subscribers) > 0:
            try:
                return [func(*args, **kwargs) for func in self.__subscribers]
            except TypeError as e:
                raise NotEnoughArgumentsError(str(e))
        else:
            raise UndersubscribedEventError("No subscribers.")