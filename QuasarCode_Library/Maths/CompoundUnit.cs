using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

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
        public UnitPowerPair[] Values { get; protected set; }

        /// <summary>
        /// Creates a new compound unit from an array of other units
        /// </summary>
        /// <param name="units">The compound units to combine</param>
        public CompoundUnit(params IGeneralUnit[] units)
        {
            List<UnitPowerPair> baseUnits = new List<UnitPowerPair>();

            foreach (IGeneralUnit unit in units)
            {
                baseUnits.AddRange(unit.GetUnitPairs());
            }

            Values = SimplifyUnits(baseUnits.ToArray());
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

            Values = SimplifyUnits(Values);
        }

        /// <summary>
        /// Creates a new compound unit from an array of UnitPowerPairs
        /// </summary>
        /// <param name="units">Array of units and their powers as UnitPowerPairs</param>
        public CompoundUnit(params UnitPowerPair[] units)
        {
            Values = SimplifyUnits(units);
        }

        /// <summary>
        /// Allows compatibility between ordenary and compound unit types by providing common access to their data
        /// </summary>
        /// <returns>An array of UnitPowerPairs representing all units in the object</returns>
        public UnitPowerPair[] GetUnitPairs()
        {
            return Values;
        }

        /// <summary>
        /// Provides a string representation of the unit
        /// </summary>
        /// <returns>The unit as a string</returns>
        public override string ToString()
        {
            if (Values.Length == 1 && Values[0].Unit == Units.NoUnit)
            {
                return "";
            }
            else
            {
                string unitString = "";

                foreach (UnitPowerPair pair in Values)
                {
                    unitString += pair.Unit.ToString() + ((pair.Power == 1) ? "" : "^" + pair.Power.ToString()) + " ";
                }

                if (unitString != "")
                {
                    // Remove the extra space
                    unitString = unitString.Remove(unitString.Length - 1);
                }

                return unitString;
            }
        }

        /// <summary>
        /// Simplifies an array of UnitPowerPairs so it contains only one instance of each unit
        /// </summary>
        /// <param name="units">The array of pairs to simplify</param>
        /// <returns>A simplified array of UnitPowerPairs</returns>
        public static UnitPowerPair[] SimplifyUnits(UnitPowerPair[] units)
        {
            List<UnitPowerPair> newUnits = new List<UnitPowerPair>();

            foreach (UnitPowerPair pair in units)
            {
                if (newUnits.Count == 0)
                {
                    newUnits.Add(pair);
                }
                else
                {
                    bool added = false;
                    for (int i = 0; i < newUnits.Count; i++)
                    {
                        if (newUnits[i].Unit == pair.Unit)
                        {
                            newUnits[i] = new UnitPowerPair { Unit = newUnits[i].Unit, Power = newUnits[i].Power + pair.Power };
                            added = true;
                            break;
                        }
                    }

                    
                    if (!added)
                    {
                        newUnits.Add(pair);
                    }
                }
                
            }

            // Remove all units with a power of 0
            bool isTarget(UnitPowerPair pair) { return pair.Power == 0; }
            newUnits.RemoveAll(new Predicate<UnitPowerPair>(isTarget));

            if (newUnits.Count == 0)
            {
                newUnits.Add(new UnitPowerPair { Unit = Units.NoUnit, Power = 0 });
            }
            else if (newUnits.Count > 1)
            {
                bool isTarget2(UnitPowerPair pair) { return pair.Unit == Units.NoUnit; }
                newUnits.RemoveAll(new Predicate<UnitPowerPair>(isTarget2));
            }

            return newUnits.ToArray();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public override bool Equals(object o)
        {
            bool result = true;

            List<UnitPowerPair> aValues = Values.OrderBy(new Func<UnitPowerPair, Units>((UnitPowerPair pair) => pair.Unit)).ToList();
            List<UnitPowerPair> bValues = ((IGeneralUnit)o).GetUnitPairs().OrderBy(new Func<UnitPowerPair, Units>((UnitPowerPair pair) => pair.Unit)).ToList();

            if (aValues.Count != bValues.Count)
            {
                return false;
            }
            else
            {
                for (int i = 0; i < Values.Length; i++)
                {
                    if (aValues[i].Unit != bValues[i].Unit || aValues[i].Power != bValues[i].Power)
                    {
                        result = false;
                        break;
                    }
                }

                return result;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator ==(CompoundUnit a, CompoundUnit b)
        {
            return a.Equals(b);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator !=(CompoundUnit a, CompoundUnit b)
        {
            return !a.Equals(b);
        }
    }
}
