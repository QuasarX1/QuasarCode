using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths
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
    }
}
