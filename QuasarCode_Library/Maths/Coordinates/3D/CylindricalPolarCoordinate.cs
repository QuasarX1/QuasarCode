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

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public CylindricalPolarCoordinate(ICoordinateSystem<CylindricalPolar> coordinateSystem, decimal r, decimal theta, decimal z)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { r, theta, z };
        }

        public Matrices.Vectors.IVector<CylindricalPolar> GetVector()
        {
            throw new NotImplementedException();
            //return new Matrices.Vectors.PolarVector<CylindricalPolar>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<CylindricalPolar> vector)
        {
            if (vector.Rows != this.Dimentions)
            {
                throw new ArgumentException("The vector provided has the wrong number of dimentions.");
            }

            decimal[] result = GetVector().Add(vector).ComponentArray;

            for (int i = 0; i < Dimentions; i++)
            {
                Ordinates[i] = result[i];
            }
        }

        new public object Clone()
        {
            return new CylindricalPolarCoordinate(this.System, this.Ordinates[0], this.Ordinates[1], this.Ordinates[2]);
        }
        
        public override string ToString()
        {
            return "(" + Ordinates[0].ToString() + ", " + Ordinates[1].ToString() + ", " + Ordinates[2].ToString() + ")";
        }
    }
}
