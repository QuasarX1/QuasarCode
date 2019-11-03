using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    public interface ISystem
    {
        string Name { get; }
        Dictionary<Tuple<IQuantity, ISystem, ISystem>, SystemConversion> Conversions { get; }
        Dictionary<IQuantity, ISingleUnit> BaseUnits { get; }
    }
}