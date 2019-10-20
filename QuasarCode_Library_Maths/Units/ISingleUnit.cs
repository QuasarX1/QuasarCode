using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ISingleUnit : IUnit
    {
        Quantities Quantity { get; }
        Systems System { get; }
        double SystemBaseMultyplier { get; }
        string Text { get; }
    }
}
