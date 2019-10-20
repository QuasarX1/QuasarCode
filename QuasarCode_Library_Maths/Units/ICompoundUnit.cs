using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ICompoundUnit : IUnit
    {
        UnitPowerPair[] UnitPowerPairs { get; }

        IUnit Simplify();
    }
}
