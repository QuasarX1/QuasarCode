from enum import Enum
from QuasarCode.Maths.Units._ISystem import ISystem
from QuasarCode.Maths.Units.Quantities import NoneQuantity, Angle, Length, Mass, Time, ElectricCurrent, Temperature, Quantity, LuminousIntensity

class Systems(Enum):
    """
    The systems of mesurement with avalable units

    none - No present system
    SI - SI or Metric
    Imperial - Imperial (Old)
    """

    # No present system
    none,

    # SI or Metric
    SI,

    # Imperial (Old)
    Imperial


class SystemBase(ISystem):
    def __init__(self, name, baseUnits, *conversions):
        self.__Name = name

        self.__BaseUnits = {}
        for unit in baseUnits:
            self.__BaseUnits[unit.getQuantity()] = unit

        self.__Conversions = {}
        for conversion in conversions:
            self.__Conversions[(conversion.getForQuantity(), conversion.getFromSystem(), conversion.getToSystem())] = conversion

        if issubclass(self, NoneSystem):
            self.__Conversions[(NoneQuantity(), self, self)] = SystemConversion(NoneQuantity(), this, this, lambda value: value)
            self.__Conversions[(Angle(), self, self)] = SystemConversion(Angle(), this, this, lambda value: value)
            self.__Conversions[(Length(), self, self)] = SystemConversion(Length(), this, this, lambda value: value)
            self.__Conversions[(Mass(), self, self)] = SystemConversion(Mass(), this, this, lambda value: value)
            self.__Conversions[(Time(), self, self)] = SystemConversion(Time(), this, this, lambda value: value)
            self.__Conversions[(ElectricCurrent(), self, self)] = SystemConversion(ElectricCurrent(), this, this, lambda value: value)
            self.__Conversions[(Temperature(), self, self)] = SystemConversion(Temperature(), this, this, lambda value: value)
            self.__Conversions[(Quantity(), self, self)] = SystemConversion(Quantity(), this, this, lambda value: value)
            self.__Conversions[(LuminousIntensity(), self, self)] = SystemConversion(LuminousIntensity(), this, this, lambda value: value)

    def getName(self):
        return self.__Name

    def getConversions(self):
        return self.__Conversions

    def getBaseUnits(self):
        return self.__BaseUnits

class NoneSystem(SystemBase):
    def __init__(self):
        super().__init__("None", [none()])

class SI(SystemBase):
    def __init__(self):
        super().__init__("SI", [Radian(), Meter(), Kilogram(), Second(), Ampere(), Kelvin(), Moles(), Candela()])

class Imperial(SystemBase):
    def __init__(self):
        super().__init__("Imperial", [])