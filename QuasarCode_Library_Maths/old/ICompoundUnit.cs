using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old
{
    /// <summary>
    /// Multiple base units with powers multiplied together to form a compound unit
    /// </summary>
    public interface ICompoundUnit : IGeneralUnit
    {
        /// <summary>
        /// The base units and their powers
        /// </summary>
        UnitPowerPair[] Values { get; }
    }
}
