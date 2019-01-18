using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public class UnitVector<T> where T : Coordinates.ICoordinateSystem
    {
        double Magnitude { get; set; }

        //Direction { get; set; }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="magnitude">The length of the vector</param>
        /// <param name="point1">A point on the line in the direction of the vector</param>
        /// <param name="point2">A point on the line in the direction of the vector</param>
        public UnitVector(Coordinates.ICoordinate point1, Coordinates.ICoordinate point2)
        {
            Magnitude = 1;

            Direction = point2 - point1;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="vector"></param>
        public UnitVector(Vector<T> vector)
        {

        }
    }
}
