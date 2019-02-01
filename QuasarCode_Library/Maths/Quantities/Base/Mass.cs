using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths._Quantities.Base
{
    /// <summary>
    /// The mesure of the matter comprising a body
    /// </summary>
    public class Mass: IQuantity
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="magnitude">The size of the mass</param>
        /// <param name="unit">The unit of mass</param>
        public Mass(double magnitude, Units unit = Units.Kg)
        {
            Magnitude = magnitude;
            Unit = unit;
        }

        /// <summary>
        /// The size of the mass
        /// </summary>
        public double Magnitude { get; set; }

        /// <summary>
        /// The unit of mass
        /// </summary>
        public Units Unit { get; set; }

        /// <summary>
        /// 
        /// </summary>
        public Units SIUnit { get { return Units.Kg; } }
    }
}
