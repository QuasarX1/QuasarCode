using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems.ND;


namespace QuasarCode.Library.Maths.Coordinates.ND
{
    public class Cartesian_ND_Coordinate : ICoordinate<Cartesian_ND>
    {
        public ICoordinateSystem<Cartesian_ND> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_ND_Coordinate(ICoordinateSystem<Cartesian_ND> coordinateSystem, params double[] ordinates)
        {
            System = coordinateSystem;

            Ordinates = ordinates;
        }

        public Vector<Cartesian_ND> GetVector()
        {

        }
    }
}
