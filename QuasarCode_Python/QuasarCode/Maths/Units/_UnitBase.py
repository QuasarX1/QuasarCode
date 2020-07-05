from QuasarCode.Maths.Units._IUnit import IUnit
from QuasarCode.Tools import StringLiterals

class UnitBase(IUnit):
    def Mult(self, u):
        return CompoundUnit.NewCompoundUnit(self.GetUnitPairs().extend(u.GetUnitPairs()))

    def Mult(self, u):
        items = self.GetUnitPairs()

        for pair in u.GetUnitPairs():
            items.append(UnitPowerPair(Unit = pair.Unit, Power = -pair.Power))

        return CompoundUnit.NewCompoundUnit(items)

    def __mul__(self, other):
        return self.Mult(other)

    def __div__(self, other):
        return self.Div(other)

    def ToString(self):
        result = ""

        for pair in self.GetFundamentalUnitPairs():
            result += pair.Unit.ToString()
            for character in pair.Power.ToString():
                if character == "-":
                    result += StringLiterals.Superscript_Minus
                else:
                    result += StringLiterals.superscriptFromNormal(character)

            result += " ";

        return result.rstrip();