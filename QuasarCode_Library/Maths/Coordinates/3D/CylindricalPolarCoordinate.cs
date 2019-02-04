using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.Coordinates._3D
{
    public class CylindricalPolarCoordinate : ICoordinate<CylindricalPolar>
    {
        public ICoordinateSystem<CylindricalPolar> System { get; }

        public double[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public CylindricalPolarCoordinate(ICoordinateSystem<CylindricalPolar> coordinateSystem, double r, double theta, double z)
        {
            System = coordinateSystem;

            Ordinates = new double[] { r, theta, z };
        }

        public Vector<CylindricalPolar> GetVector()
        {

        }
    }
}
