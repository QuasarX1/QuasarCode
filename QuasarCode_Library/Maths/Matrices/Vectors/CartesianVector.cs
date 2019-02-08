using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public class CartesianVector<T> : NMatrix, IVector where T : Coordinates.Systems.ICartesianBase<T>
    {
        public NMatrix Components { get; }

        public decimal[] ComponentArray
        {
            get
            {
                decimal[] result = new decimal[this.Rows];
                for (int i = 0; i < this.Rows; i++)
                {
                    result[i] = this.Data[i, 0];
                }
                return result;
            }
        }

        public decimal Magnitude
        {
            get
            {
                decimal sum = 0;
                for (int i = 0; i < Components.Rows; i++)
                {
                    sum += (decimal)Math.Pow((double)Components[i, 0], 2);
                }

                return (decimal)Math.Sqrt((double)sum);
            }
            set
            {
                // Use matrix to ajust components to produce requested mag
                // or just find mag. ratio...
            }
        }

        public CartesianVector(params decimal[] components) : base(GridFromArray(components)) { }

        public CartesianVector(Coordinates.ICoordinate<T> point1, Coordinates.ICoordinate<T> point2) : base(new double[0, 0])
        {
            if (point1.Dimentions != point2.Dimentions)
            {
                throw new ArgumentException("Coordinates provided belonged to cartesian systems with different numbers of dimentions.");
            }

            Data = new decimal[point1.Dimentions, 1];
            for (int i = 0; i < point1.Dimentions; i++)
            {
                Data[i, 0] = point2.Ordinates[i] - point1.Ordinates[i];
            }

            Rows = point1.Dimentions;
            Columns = 1;
        }

        public CartesianVector(CartesianVector<T> vector) : base(vector.Data) { }

        public static string[] ComponentIdentifiers = new string[] { "i", "j", "k", "l", "m", "n", "o", "p" };

        new public string ToString()
        {
            string result = "";

            for (int i = 0; i < Rows; i++)
            {
                if (Data[i, 0] != 0)
                {
                    result += Data[i, 0] + " " + ComponentIdentifiers[i] + ", ";
                }
            }

            result = result.Remove(result.Length - 2);

            return result;
        }

        public string[] GetComponentStrings()
        {
            string[] result = new string[Rows];

            for (int i = 0; i < Rows; i++)
            {
                if (Data[i, 0] != 0)
                {
                    result[i] = Data[i, 0] + " " + ComponentIdentifiers[i];
                }
            }

            return result;
        }

        public static decimal[,] GridFromArray(decimal[] array)
        {
            decimal[,] result = new decimal[array.Length, 1];

            for (int i = 0; i < array.Length; i++)
            {
                result[i, 0] = array[i];
            }

            return result;
        }

        public decimal Dot(IVector vector)
        {
            return base.Dot(vector);
        }

        public IVector Cross(IVector vector)
        {
            if (this.Rows != vector.Rows || this.Columns != vector.Columns)
            {
                throw new ArgumentException("Vector cross multiplication failed - vectors had different shapes.");
            }

            decimal[,] combinedData = new decimal[3, this.Columns];
            for (int i = 0; i < this.Columns; i++)
            {
                combinedData[0, i] = 1;
                combinedData[1, i] = this.Data[i, 0];
                combinedData[2, i] = vector[i];
            }

            NMatrix cofactors = new NMatrix(combinedData).Cofactors();

            decimal[] components = new decimal[cofactors.Columns];
            for (int i = 0; i < cofactors.Columns; i++)
            {
                components[i] = cofactors[0, i];
            }

            return new CartesianVector<T>(components);
        }

        public decimal this[int row] { get { return this.Data[row, 0]; } }
    }
}