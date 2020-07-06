from enum import Enum
from QuasarCode.Maths.Units._IQuantity import IQuantity

class Quantities(Enum):
    """
    Physical quantitys that have units

    none - No assigned quantity
    Angle - Mesurement of rotation
    Length - Mesurement of space
    Mass - Mesurement of matter
    Time - Mesurement of change
    ElectricCurrent - Mesurement of electricity
    Temperature - Mesurement of thermal energy
    Quantity - Mesurement of quantity
    LuminousIntensity - Mesurement of electromagnitism
    """

    # No assigned quantity
    none,

    # Mesurement of rotation
    Angle,

    # Mesurement of space
    Length,

    # Mesurement of matter
    Mass,

    # Mesurement of change
    Time,

    # Mesurement of electricity
    ElectricCurrent,

    # Mesurement of thermal energy
    Temperature,

    # Mesurement of quantity
    Quantity,

    # Mesurement of electromagnitism
    LuminousIntensity


class QuantityBase(IQuantity):
    def __init__(self, name):
        self.__Name = name

    def getName(self):
        return self.__Name


class NoneQuantity(QuantityBase):
    def __init__(self):
        super().__init__("None")

class Angle(QuantityBase):
    def __init__(self):
        super().__init__("Angle")

class Length(QuantityBase):
    def __init__(self):
        super().__init__("Length")

class Mass(QuantityBase):
    def __init__(self):
        super().__init__("Mass")

class Time(QuantityBase):
    def __init__(self):
        super().__init__("Time")

class ElectricCurrent(QuantityBase):
    def __init__(self):
        super().__init__("ElectricCurrent")

class Temperature(QuantityBase):
    def __init__(self):
        super().__init__("Temperature")

class Quantity(QuantityBase):
    def __init__(self):
        super().__init__("Quantity")

class LuminousIntensity(QuantityBase):
    def __init__(self):
        super().__init__("LuminousIntensity")