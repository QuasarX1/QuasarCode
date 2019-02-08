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

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_3D_Coordinate(ICoordinateSystem<Cartesian_3D> coordinateSystem, decimal x, decimal y, decimal z)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { x, y, x };
        }

        public Matrices.Vectors.IVector GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Cartesian_3D>(Ordinates);
        }
    }
}
