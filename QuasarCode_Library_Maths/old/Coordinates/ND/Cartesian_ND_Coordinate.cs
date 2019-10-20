using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

using QuasarCode.Library.Maths.old.Coordinates.Systems;
using QuasarCode.Library.Maths.old.Coordinates.Systems.ND;


namespace QuasarCode.Library.Maths.old.Coordinates.ND
{
    public class Cartesian_ND_Coordinate : ICoordinate<Cartesian_ND>
    {
        public ICoordinateSystem<Cartesian_ND> System { get; }

        public decimal[] Ordinates { get; }

        public int Dimentions { get { return System.Dimentions; } }

        public Cartesian_ND_Coordinate(ICoordinateSystem<Cartesian_ND> coordinateSystem, params decimal[] ordinates)
        {
            if (ordinates.Length != coordinateSystem.Dimentions)
            {
                throw new ArgumentException("Coordinate creation failed - number of ordinates provided was inapropriate for the number of dimentions in the coordinate system.");
            }

            System = coordinateSystem;

            Ordinates = ordinates;
        }

        public Matrices.Vectors.IVector<Cartesian_ND> GetVector()
        {
            return new Matrices.Vectors.CartesianVector<Cartesian_ND>(Ordinates);
        }

        public void Move(Matrices.Vectors.IVector<Cartesian_ND> vector)
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
            return new Cartesian_ND_Coordinate(this.System, (decimal[])this.Ordinates.Clone());
        }

        public override string ToString()
        {
            if (Ordinates.Length > 0)
            {
                return "(" + (from item in Ordinates.Take(Ordinates.Length - 2) select item.ToString() + ", ").ToString() + Ordinates[Ordinates.Length - 1].ToString() + ")";
            }
            else
            {
                return "";
            }
        }
    }
}
