using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.Coordinates._3D
{
    public class SphericalPolarCoordinate : ICoordinate<SphericalPolar>
    {
        public ICoordinateSystem<SphericalPolar> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public SphericalPolarCoordinate(ICoordinateSystem<SphericalPolar> coordinateSystem, double r, double theta, double phi)
        {
            System = coordinateSystem;

            Ordinates = new double[] { r, theta, phi };
        }

        public Vector<SphericalPolar> GetVector()
        {

        }
    }
}
