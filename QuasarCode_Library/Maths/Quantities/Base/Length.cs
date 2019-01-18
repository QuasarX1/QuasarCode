using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Quantities.Base
{
    public class Length<T>: IVectorQuantity<T> where T : Coordinates.ICoordinateSystem
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="magnitude">The size of the mass</param>
        /// <param name="unit">The unit of mass</param>
        public Length(double magnitude, Units unit = Units.Kg, T direction)
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
