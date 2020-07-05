using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// A unit paired with a power
    /// </summary>
    public struct FundamentalUnitPowerPair
    {
        /// <summary>
        /// The unit
        /// </summary>
        public ISingleUnit Unit;

        /// <summary>
        /// The power
        /// </summary>
        public int Power;

        public static bool operator ==(FundamentalUnitPowerPair a, FundamentalUnitPowerPair b)
        {
            return a.Power == b.Power && a.Unit == b.Unit;
        }

        public static bool operator !=(FundamentalUnitPowerPair a, FundamentalUnitPowerPair b)
        {
            return !(a == b);
        }

        public static implicit operator UnitPowerPair(FundamentalUnitPowerPair instance)
        {
            return new UnitPowerPair { Unit = instance.Unit, Power = instance.Power };
        }
    }
}