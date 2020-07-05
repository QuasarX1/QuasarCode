using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Coordinates.Systems._2D;

namespace QuasarCode.Library.Maths.old.Coordinates._2D
{
    public class Cartesian_2D_Coordinate : ICoordinate<Cartesian_2D>
    {
        public ICoordinateSystem<Cartesian_2D> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_2D_Coordinate(ICoordinateSystem<Cartesian_2D> coordinateSystem, decimal x, decimal y)
        {
            System = coordinateSystem;

            Ordinates = new decimal[] { x, y };
        }

        public Matrices.Vectors.IVector<Cartesian_2D> GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Cartesian_2D>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<Cartesian_2D> vector)
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
            return new Cartesian_2D_Coordinate(this.System, this.Ordinates[0], this.Ordinates[1]);
        }

        public override string ToString()
        {
            return "(" + Ordinates[0].ToString() + ", " + Ordinates[1].ToString() + ")";
        }
    }
}
