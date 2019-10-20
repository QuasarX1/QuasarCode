using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Units
{
    /// <summary>
    /// A unit paired with a power
    /// </summary>
    public struct UnitPowerPair
    {
        /// <summary>
        /// The unit
        /// </summary>
        public ISingleUnit Unit;

        /// <summary>
        /// The power
        /// </summary>
        public int Power;
    }
}
