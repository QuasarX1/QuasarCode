using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Quantities
{
    /// <summary>
    /// 
    /// </summary>
    public interface IQuantity
    {
        /// <summary>
        /// 
        /// </summary>
        double Magnitude { get; set; }

        /// <summary>
        /// 
        /// </summary>
        Units Unit { get; set; }

        /// <summary>
        /// 
        /// </summary>
        Units SIUnit { get; }
}
}
