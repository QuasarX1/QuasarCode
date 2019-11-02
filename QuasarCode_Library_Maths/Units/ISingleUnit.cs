using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ISingleUnit : IUnit, ISymbolUnit
    {
        Quantities Quantity { get; }
        Systems System { get; }

        double ConvertToSystemBase(double value);
        double ConvertFromSystemBase(double value);
    }
}