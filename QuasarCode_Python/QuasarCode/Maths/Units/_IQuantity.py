class IQuantity(object):
    def getName(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")