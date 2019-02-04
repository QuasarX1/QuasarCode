using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._2D;

namespace QuasarCode.Library.Maths.Coordinates._2D
{
    public class PolarCoordinate : ICoordinate<Polar>
    {
        public ICoordinateSystem<Polar> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public PolarCoordinate(ICoordinateSystem<Polar> coordinateSystem, double r, double theta)
        {
            System = coordinateSystem;

            Ordinates = new double[] { r, theta };
        }

        public Vector<Polar> GetVector()
        {

        }
    }
}
