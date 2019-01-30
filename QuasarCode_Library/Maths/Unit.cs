using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// A single base unit with an optional power
    /// </summary>
    public class Unit : IUnit
    {
        /// <summary>
        /// The base unit
        /// </summary>
        public Units Value { get; }

        /// <summary>
        /// The power on the unit
        /// </summary>
        public int Power { get; }

        /// <summary>
        /// Creates a new base unit with an optional power
        /// </summary>
        /// <param name="value">The base unit</param>
        /// <param name="power">The power on the unit. Deafult is 1</param>
        public Unit(Units value, int power = 1)
        {
            Value = value;

            Power = power;
        }

        /// <summary>
        /// Allows compatibility between ordenary and compound unit types by providing common access to their data
        /// </summary>
        /// <returns>An array of UnitPowerPairs representing all units in the object</returns>
        public UnitPowerPair[] GetUnitPairs()
        {
            return new UnitPowerPair[1] { new UnitPowerPair() { Unit = Value, Power = Power } };
        }
    }
}
