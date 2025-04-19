class MultiItterator(object):
    """
    Allows for itteration of multiple collections similtaniously.
    Produces a tuple with the first element being the index used and the other
    items being the corisponding elements from the collections provided.

    Arguments:
        params[collection] collections -> Collections of the same length to itterate through.
    """

    def __init__(self, *collections):
        self.__items = tuple(collections)
        self.__length = len(self.__items[0])
        self.__nextIndex = 0

        sameLength = True
        for i in range(1, len(self.__items)):
            if len(self.__items[i]) != self.__length:
                sameLength = False
                break

            if not sameLength:
                raise ValueError("The colections provided were not all of the same length.")

    def __len__(self):
        return self.__length

    def __iter__(self):
        self.__nextIndex = 0
        return self

    def __next__(self):
        """
        Returns:
            tuple -> (index, item1[index], item2[index], ...)
        """
        if self.__nextIndex < self.__length:
            index = self.__nextIndex
            self.__nextIndex += 1
            return (index, *[collection[index] for collection in self.__items])
        else:
            raise StopIteration