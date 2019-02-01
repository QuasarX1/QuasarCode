using System;
using System.Collections.Generic;
using System.Text;
using QuasarCode.Library.Maths.Matrices.Vectors;

namespace QuasarCode.Library.Maths._Quantities.Base
{
    /// <summary>
    /// 
    /// </summary>
    /// <typeparam name="T"></typeparam>
    public class Angle<T>: IVectorQuantity<T> where T : Coordinates.Systems.ICoordinateSystem
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="magnitude">The size of the mass</param>
        /// <param name="unit">The unit of mass</param>
        public Angle(double magnitude, Units unit = Units.Kg)
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

        /// <summary>
        /// 
        /// </summary>
        public Vector<T> Direction { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }
    }
}
