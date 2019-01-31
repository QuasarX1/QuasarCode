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
        public int StandardPower { get; protected set; }

        /// <summary>
        /// Creates a new value, altering the provided value and power (if nessessary) to express the value in standard form
        /// </summary>
        /// <param name="size">The size of the value</param>
        /// <param name="standardPower">The standard form power (for the provided value).</param>
        /// <param name="unit">The unit</param>
        public StandardValue(double size, IGeneralUnit unit, int standardPower = 0) : base(size, unit)
        {
            StandardPower = standardPower;

            while (!(Magnitude >= 0 && Magnitude < 10))
            {
                if (Magnitude < 0)
                {
                    Magnitude *= 10;
                    StandardPower -= 1;
                }
                else// Magnitude >= 10
                {
                    Magnitude /= 10;
                    StandardPower += 1;
                }
            }
        }

        /// <summary>
        /// Creates a new value, altering the provided value and power (if nessessary) to express the value in standard form
        /// </summary>
        /// <param name="size">The size of the value</param>
        /// <param name="standardPower">The standard form power (for the provided value)</param>
        /// <param name="unit">The unit</param>
        /// <param name="unitPower">The unit's power</param>
        public StandardValue(double size, Units unit, int standardPower = 0, int unitPower = 1) : base(size, unit, unitPower)
        {
            StandardPower = standardPower;

            while (!(Magnitude >= 0 && Magnitude < 10))
            {
                if (Magnitude < 0)
                {
                    Magnitude *= 10;
                    StandardPower -= 1;
                }
                else// Magnitude >= 10
                {
                    Magnitude /= 10;
                    StandardPower += 1;
                }
            }
        }

        /// <summary>
        /// Returns the value's actual magnitude. This should be overrided in child classes to provide the magnitude as a single value for arithmatic operations
        /// </summary>
        /// <returns>The magnitude of the value</returns>
        public override double GetMagnitude()
        {
            return Magnitude * Math.Pow(10, StandardPower);
        }

        /// <summary>
        /// Provides a string representation of the value with its unit
        /// </summary>
        /// <returns>The value as a string</returns>
        public override string ToString()
        {
            return Magnitude.ToString() + ((StandardPower != 0) ?  " x 10^" + StandardPower : "") + ((Unit.ToString() != "") ? " " + Unit.ToString() : "");
        }

        /// <summary>
        /// Converts to a Value object without standard form
        /// </summary>
        /// <returns>A new Value object</returns>
        public Value ToValue()
        {
            return new Value(GetMagnitude(), Unit);
        }

        /// <summary>
        /// Raise the standard value to an integer power
        /// </summary>
        /// <param name="a">The standard value</param>
        /// <param name="b">Integer power</param>
        /// <returns></returns>
        public static StandardValue operator ^(StandardValue a, int b)
        {
            a.Magnitude *= b;
            a.StandardPower *= b;
            //a.Unit ^= b;

            return a;
        }
    }
}
