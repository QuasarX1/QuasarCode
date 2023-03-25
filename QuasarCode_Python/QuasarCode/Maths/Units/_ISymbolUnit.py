from QuasarCode.Maths.Units._IUnit import IUnit

class ISymbolUnit(IUnit):
    def getText(self):
        raise NotImplementedError("This method MUST be overriden in a child class.")