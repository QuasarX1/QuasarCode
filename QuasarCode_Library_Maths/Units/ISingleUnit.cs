using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ISingleUnit : IUnit, ISymbolUnit
    {
        IQuantity Quantity { get; }
        ISystem System { get; }

        double ConvertToSystemBase(double value);
        double ConvertFromSystemBase(double value);
    }
}