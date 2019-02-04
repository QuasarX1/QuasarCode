using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._1D;

namespace QuasarCode.Library.Maths.Coordinates._1D
{
    public class Coordinate_1D : ICoordinate<Line>
    {
        public ICoordinateSystem<Line> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Coordinate_1D(ICoordinateSystem<Line> coordinateSystem, double x)
        {
            System = coordinateSystem;

            Ordinates = new double[] { x };
        }

        public Vector<Line> GetVector()
        {

        }
    }
}
