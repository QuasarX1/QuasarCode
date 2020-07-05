using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old
{
    /// <summary>
    /// A value associated with a unit
    /// </summary>
    public interface IValue
    {
        /// <summary>
        /// The unit
        /// </summary>
        IGeneralUnit Unit { get; }

        /// <summary>
        /// The size of the value
        /// </summary>
        double Magnitude { get; }

        /// <summary>
        /// Returns the value's actual magnitude. This should be overrided in child classes to provide the magnitude as a single value for arithmatic operations
        /// </summary>
        /// <returns>The magnitude of the value</returns>
        double GetMagnitude();

        /// <summary>
        /// Converts the value to one with an equivilant unit
        /// </summary>
        /// <param name="unit">The new value's units</param>
        /// <returns>The corisponding IValue object</returns>
        IValue As(Units unit);

        /// <summary>
        /// Converts the value to one with an equivilant unit
        /// </summary>
        /// <param name="unit">The new value's units</param>
        /// <returns>The corisponding IValue object</returns>
        IValue As(IGeneralUnit unit);

        /// <summary>
        /// Raises a value to a power
        /// </summary>
        /// <param name="p">The power</param>
        /// <returns>A new value</returns>
        IValue Pow(int p);

        /// <summary>
        /// Rounds the value to the provided number of decimal places provided
        /// </summary>
        /// <param name="digits">The number of decimal places to round to.</param>
        /// <returns>A new IValue instance with the rounded value</returns>
        IValue Round(int digits);
    }
}
