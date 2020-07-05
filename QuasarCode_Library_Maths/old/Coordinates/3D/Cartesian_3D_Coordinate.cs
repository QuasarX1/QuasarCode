using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Coordinates.Systems._3D;


namespace QuasarCode.Library.Maths.old.Coordinates._3D
{
    public class Cartesian_3D_Coordinate : ICoordinate<Cartesian_3D>
    {
        public ICoordinateSystem<Cartesian_3D> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_3D_Coordinate(ICoordinateSystem<Cartesian_3D> coordinateSystem, decimal x, decimal y, decimal z)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { x, y, z };
        }

        public Matrices.Vectors.IVector<Cartesian_3D> GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Cartesian_3D>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<Cartesian_3D> vector)
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
            return new Cartesian_3D_Coordinate(this.System, this.Ordinates[0], this.Ordinates[1], this.Ordinates[2]);
        }

        public override string ToString()
        {
            return "(" + Ordinates[0].ToString() + ", " + Ordinates[1].ToString() + ", " + Ordinates[2].ToString() + ")";
        }
    }
}
