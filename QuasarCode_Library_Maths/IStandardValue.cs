using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
{
    /// <summary>
    /// A value in standard form associated with a unit
    /// </summary>
    public interface IStandardValue : IValue
    {
        /// <summary>
        /// The standard form power
        /// </summary>
        int StandardPower { get;  }

        /// <summary>
        /// Provides a string representation of the value with its unit
        /// </summary>
        /// <returns>The value as a string</returns>
        string ToString();

        /// <summary>
        /// Raises a standard value to a power
        /// </summary>
        /// <param name="p">The power</param>
        /// <returns>A new standard value</returns>
        new IStandardValue Pow(int p);

        /// <summary>
        /// Rounds the value to the provided number of decimal places provided
        /// </summary>
        /// <param name="digits">The number of decimal places to round to.</param>
        /// <returns>A new IStandardValue instance with the rounded value</returns>
        new IStandardValue Round(int digits);
    }
}
