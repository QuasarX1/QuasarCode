from QuasarCode.Maths.Units._ISymbolUnit import ISymbolUnit

class ISingleUnit(ISymbolUnit):
    def getQuantity(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def getSystem(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def ConvertToSystemBase(value, power = 1):
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def ConvertFromSystemBase(value, power = 1):
        raise NotImplementedError("This method MUST be overriden in a child class.")