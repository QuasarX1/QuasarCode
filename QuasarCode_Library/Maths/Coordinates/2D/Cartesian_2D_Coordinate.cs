using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._2D;

namespace QuasarCode.Library.Maths.Coordinates._2D
{
    public class Cartesian_2D_Coordinate : ICoordinate<Cartesian_2D>
    {
        public ICoordinateSystem<Cartesian_2D> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_2D_Coordinate(ICoordinateSystem<Cartesian_2D> coordinateSystem, double x, double y)
        {
            System = coordinateSystem;

            Ordinates = new double[] { x, y };
        }

        public Vector<Cartesian_2D> GetVector()
        {

        }
    }
}
