using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// A value in standard form associated with a unit
    /// </summary>
    public class StandardValue : Value, IStandardValue
    {
        /// <summary>
        /// The standard form power
        /// </summary>
        public int StandardPower { get; }

        /// <summary>
        /// Creates a new value, altering the provided value and power (if nessessary) to express the value in standard form
        /// </summary>
        /// <param name="size">The size of the value</param>
        /// <param name="standardPower">The standard form power (for the provided value)</param>
        /// <param name="unit">The unit</param>
        public StandardValue(double size, int standardPower, IGeneralUnit unit) : base(size, unit)
        {
            StandardPower = standardPower;
        }

        /// <summary>
        /// Creates a new value, altering the provided value and power (if nessessary) to express the value in standard form
        /// </summary>
        /// <param name="size">The size of the value</param>
        /// <param name="standardPower">The standard form power (for the provided value)</param>
        /// <param name="unit">The unit</param>
        /// <param name="unitPower">The unit's power</param>
        public StandardValue(double size, int standardPower, Units unit, int unitPower = 1) : base(size, unit, unitPower)
        {
            StandardPower = standardPower;
        }

        /// <summary>
        /// Returns the value's actual magnitude. This should be overrided in child classes to provide the magnitude as a single value for arithmatic operations
        /// </summary>
        /// <returns></returns>
        protected override double GetMagnitude()
        {
            return Magnitude * (10 ^ StandardPower);
        }

        /// <summary>
        /// Converts to a Value object without standard form
        /// </summary>
        /// <returns>A new Value object</returns>
        public Value ToValue()
        {
            return new Value(GetMagnitude(), Unit);
        }
    }
}
