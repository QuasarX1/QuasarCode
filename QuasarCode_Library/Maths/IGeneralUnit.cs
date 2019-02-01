using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// Blank interface to provide a link between ordenary and compound unit types
    /// </summary>
    public interface IGeneralUnit
    {
        /// <summary>
        /// Allows compatibility between ordenary and compound unit types by providing common access to their data
        /// </summary>
        /// <returns>An array of UnitPowerPairs representing all units in the object</returns>
        UnitPowerPair[] GetUnitPairs();

        /// <summary>
        /// Provides a string representation of the unit
        /// </summary>
        /// <returns>The unit as a string</returns>
        string ToString();

        /// <summary>
        /// Raises a unit to a power
        /// </summary>
        /// <param name="p">The power</param>
        /// <returns>A new IGeneralUnit instance</returns>
        IGeneralUnit Pow(int p);
    }
}
