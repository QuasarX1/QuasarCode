using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old
{
    /// <summary>
    /// A single base unit with an optional power
    /// </summary>
    public interface IUnit : IGeneralUnit
    {
        /// <summary>
        /// The base unit
        /// </summary>
        Units Value { get; }

        /// <summary>
        /// The power on the unit
        /// </summary>
        int Power { get; }
    }
}
