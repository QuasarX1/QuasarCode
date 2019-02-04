using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.Coordinates._3D
{
    public class Cartesian_3D_Coordinate : ICoordinate<Cartesian_3D>
    {
        public ICoordinateSystem<Cartesian_3D> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_3D_Coordinate(ICoordinateSystem<Cartesian_3D> coordinateSystem, double x, double y, double z)
        {
            System = coordinateSystem;

            Ordinates = new double[] { x, y, x };
        }

        public Vector<Cartesian_3D> GetVector()
        {

        }
    }
}
