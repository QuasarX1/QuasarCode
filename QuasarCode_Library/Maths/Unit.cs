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
                return Value.ToString() + "^" + Power.ToString();
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator ==(Unit a, Unit b)
        {
            return a.Value == b.Value && a.Power == b.Power;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns></returns>
        public static bool operator !=(Unit a, Unit b)
        {
            return a.Value != b.Value || a.Power != b.Power;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="o"></param>
        /// <returns></returns>
        public override bool Equals(object o)
        {
            return base.Equals(o);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public override int GetHashCode()
        {
            return base.GetHashCode();
        }
    }
}
