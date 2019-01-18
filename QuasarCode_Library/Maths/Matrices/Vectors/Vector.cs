using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    /// <summary>
    /// 
    /// </summary>
    /// <typeparam name="T">Coordinate system</typeparam>
    public class Vector<T> where T: Coordinates.Systems.ICoordinateSystem
    {
        double Magnitude { get; set; }

        UnitVector<T> Direction { get; set; }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="magnitude">The length of the vector</param>
        /// <param name="point1">A point on the line in the direction of the vector</param>
        /// <param name="point2">A point on the line in the direction of the vector</param>
        public Vector(double magnitude, Coordinates.ICoordinate point1, Coordinates.ICoordinate point2)
        {
            Magnitude = magnitude;

            Direction = new UnitVector<T>(point1, point2);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="magnitude"></param>
        /// <param name="direction"></param>
        public Vector(double magnitude, UnitVector<T> direction)
        {
            Magnitude = magnitude;
            Direction = direction;
        }
    }
}
