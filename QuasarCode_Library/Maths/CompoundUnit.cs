using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// Multiple base units with powers multiplied together to form a compound unit
    /// </summary>
    public class CompoundUnit : ICompoundUnit
    {
        /// <summary>
        /// The base units and their powers
        /// </summary>
        public UnitPowerPair[] Values { get; }

        /// <summary>
        /// Creates a new compound unit from an array of other units
        /// </summary>
        /// <param name="units">The compound units to combine</param>
        public CompoundUnit(params IGeneralUnit[] units)
        {
            List<UnitPowerPair> baseUnits = new List<UnitPowerPair>();

            foreach (ICompoundUnit unit in units)
            {
                baseUnits.AddRange(unit.GetUnitPairs());
            }

            Values = baseUnits.ToArray();
        }

        /// <summary>
        /// Creates a new compound unit from an array of tuples containing units and their corisponding powers
        /// </summary>
        /// <param name="units">Array of units and their powers as Tuples</param>
        public CompoundUnit(params Tuple<Units, int>[] units)
        {
            Values = new UnitPowerPair[units.Length];

            for (int i = 0; i < units.Length; i++)
            {
                Values[i] = new UnitPowerPair { Unit = units[i].Item1, Power = units[i].Item2 };
            }
        }

        /// <summary>
        /// Creates a new compound unit from an array of UnitPowerPairs
        /// </summary>
        /// <param name="units">Array of units and their powers as UnitPowerPairs</param>
        public CompoundUnit(params UnitPowerPair[] units)
        {
            Values = units;
        }

        /// <summary>
        /// Allows compatibility between ordenary and compound unit types by providing common access to their data
        /// </summary>
        /// <returns>An array of UnitPowerPairs representing all units in the object</returns>
        public UnitPowerPair[] GetUnitPairs()
        {
            return Values;
        }
    }
}
