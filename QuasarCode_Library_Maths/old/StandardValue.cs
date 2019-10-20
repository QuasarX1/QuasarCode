using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old
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

            NormaliseValue();
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

            NormaliseValue();
        }

        /// <summary>
        /// Alter the Magnitude and Power so that the value is in standard form
        /// </summary>
        protected void NormaliseValue()
        {
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
        /// Raises a standard value to a power
        /// </summary>
        /// <param name="p">The power</param>
        /// <returns>A new standard value</returns>
        new public IStandardValue Pow(int p)
        {
            return this ^ p;
        }

        /// <summary>
        /// Rounds the value to the provided number of decimal places provided. Uses Math.Round()
        /// </summary>
        /// <param name="digits">The number of decimal places to round to.</param>
        /// <returns>A new StandardValue object with the rounded value</returns>
        public new IStandardValue Round(int digits)
        {
            return new StandardValue(Math.Round(this.Magnitude, digits, MidpointRounding.AwayFromZero), this.Unit, this.StandardPower);
        }

        /// <summary>
        /// Provides a string representation of the value with its unit
        /// </summary>
        /// <returns>The value as a string</returns>
        public override string ToString()
        {
            string power = "";
            foreach (char num in StandardPower.ToString())
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
            
            return Magnitude.ToString() + ((StandardPower != 0) ?  " x 10" + power : "") + ((Unit.ToString() != "") ? " " + Unit.ToString() : "");
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
            StandardValue result = new StandardValue(a.Magnitude, a.Unit, a.StandardPower);

            result.Magnitude = Math.Pow(result.Magnitude, b);
            result.StandardPower *= b;
            result.Unit = a.Unit.Pow(b);

            result.NormaliseValue();

            return result;
        }
    }
}
