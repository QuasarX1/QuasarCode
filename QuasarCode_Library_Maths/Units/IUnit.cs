using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// Provides a link between ordenary and compound unit types
    /// </summary>
    public partial interface IUnit
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
        /// <returns>IUnit</returns>
        IUnit Pow(int p);

        /// <summary>
        /// Multiplies a unit by annother
        /// </summary>
        /// <param name="u">The unit to multyply by</param>
        /// <returns>IUnit</returns>
        IUnit Mult(IUnit u);

        /// <summary>
        /// Divides a unit by annother
        /// </summary>
        /// <param name="u">The unit to divide this by</param>
        /// <returns>IUnit</returns>
        IUnit Div(IUnit u);
    }
}
