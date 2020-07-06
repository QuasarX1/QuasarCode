from QuasarCode.Maths.Units._UnitBase import UnitBase
from QuasarCode.Maths.Units._ISingleUnit import ISingleUnit
from QuasarCode.Maths.Units._IQuantity import IQuantity
from QuasarCode.Maths.Units.Quantities import Quantities, NoneQuantity, Angle, Length, Mass, Time, ElectricCurrent, Temperature, Quantity, LuminousIntensity
from QuasarCode.Maths.Units._ISystem import ISystem
from QuasarCode.Maths.Units.Systems import Systems, NoneSystem, SI, Imperial

class SingleUnitBase(UnitBase, ISingleUnit):
    def __init__(self, quantity, system, text, systemBaseMultyplier, toBaseDeligate = None, fromBaseDeligate = None):
        if issubclass(quantity, IQuantity):
            self.__Quantity = quantity
        else:
            if quantity == Quantities.none:
                self.__Quantity = NoneQuantity()
            if quantity == Quantities.Angle:
                self.__Quantity = Angle()
            if quantity == Quantities.Length:
                self.__Quantity = Length()
            if quantity == Quantities.Mass:
                self.__Quantity = Mass()
            if quantity == Quantities.Time:
                self.__Quantity = Time()
            if quantity == Quantities.ElectricCurrent:
                self.__Quantity = ElectricCurrent()
            if quantity == Quantities.Temperature:
                self.__Quantity = Temperature()
            if quantity == Quantities.Quantity:
                self.__Quantity = Quantity()
            if quantity == Quantities.LuminousIntensity:
                self.__Quantity = LuminousIntensity()
            else:
                pass

        if issubclass(system, ISystem):
            self.__System = system
        else:
            if system == Systems.none:
                self.__System = NoneSystem()
            if system == Systems.SI:
                self.__System = SI()
            if system == Systems.Imperial:
                self.__System = Imperial()
            else:
                pass

        self.__Text = text

        self.__UnderlyingConvertToSystemBase = toBaseDeligate if toBaseDeligate is not None else lambda value, int: value / systemBaseMultyplier**power#Func<double, int, double>
        self.__UnderlyingConvertFromSystemBase = fromBaseDeligate if fromBaseDeligate is not None else lambda value, int: value * systemBaseMultyplier**power#Func<double, int, double>

    def getQuantity(self):
        return self.__Quantity

    def getSystem(self):
        return self.__System

    def getText(self):
        return self.__Text

    def GetFundamentalUnitPairs(self):
        return [FundamentalUnitPowerPair(Unit = self, Power = 1)]

    def GetUnitPairs(self):
        return [UnitPowerPair(Unit = self, Power = 1)]

    def ConvertToSystemBase(value, power = 1):
        return self.__UnderlyingConvertToSystemBase(value, power)

    def ConvertFromSystemBase(value, power = 1):
        return self.__UnderlyingConvertFromSystemBase(value, power)

    def Pow(p):
        return CompoundUnit.NewCompoundUnit([UnitPowerPair(Unit = self, Power = p)]);
    
    def ToString(self):
        return self.__Text