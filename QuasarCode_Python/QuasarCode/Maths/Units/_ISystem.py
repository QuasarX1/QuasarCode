class ISystem(object):
    def getName(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def getConversions(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def getBaseUnits(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")