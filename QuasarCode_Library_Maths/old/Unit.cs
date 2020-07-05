using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.old
{
    /// <summary>
    /// A single base unit with an optional power
    /// </summary>
    public class Unit : IUnit
    {
        /// <summary>
        /// The base unit
        /// </summary>
        public Units Value { get; protected set; }

        /// <summary>
        /// The power on the unit
        /// </summary>
        public int Power { get; protected set; }

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

        /// <summary>
        /// Provides a string representation of the unit
        /// </summary>
        /// <returns>The unit as a string</returns>
        public override string ToString()
        {
            if (Power == 0)
            {
                return "";
            }
            else if (Power == 1)
            {
                return Value.ToString();
            }
            else
            {
                string power = "";
                foreach (char num in Power.ToString())
                {
                    if (num == '-')
                    {
                        power += Tools.StringLiterals.Superscript_Minus;
                    }
                    else
                    {
                        power += Tools.StringLiterals.SuperscriptInt[int.Parse((num.ToString()))];
                    }
                }

                return Value.ToString() + power;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public override bool Equals(object o)
        {
            List<UnitPowerPair> aValues = GetUnitPairs().ToList();
            List<UnitPowerPair> bValues = ((IGeneralUnit)o).GetUnitPairs().OrderBy(new Func<UnitPowerPair, Units>((UnitPowerPair pair) => pair.Unit)).ToList();

            if (bValues.Count != 1)
            {
                return false;
            }
            else if (aValues[0].Unit != bValues[0].Unit || aValues[0].Power != bValues[0].Power)
            {
                return false;
            }
            else
            {
                return true;
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
        public static bool operator ==(Unit a, Unit b)
        {
            return a.Equals(b);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator !=(Unit a, Unit b)
        {
            return !a.Equals(b);
        }

        /// <summary>
        /// Converts a single unit from the Units enum to a Unit object with a power of 1
        /// </summary>
        /// <param name="o"></param>
        public static implicit operator Unit(Units o)
        {
            return new Unit(o);
        }

        /// <summary>
        /// Raises a unit to a power
        /// </summary>
        /// <param name="p">The power</param>
        /// <returns>A new IGeneralUnit instance</returns>
        public IGeneralUnit Pow(int p)
        {
            return new Unit(Value, Power * p);
        }
    }
}
