using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ISingleUnit : IUnit, ISymbolUnit
    {
        IQuantity Quantity { get; }
        ISystem System { get; }

        double ConvertToSystemBase(double value, int power = 1);
        double ConvertFromSystemBase(double value, int power = 1);
    }
}