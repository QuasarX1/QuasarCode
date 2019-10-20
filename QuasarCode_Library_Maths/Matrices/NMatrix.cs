using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Maths.Matrices
{
    public class NMatrix : IMatrix
    {
        protected decimal[,] Data { get; set; }

        public decimal[,] GetData()
        {
            return (decimal[,])this;
        }

        protected static double[,] DecimalsToDoubles(decimal[,] array)
        {
            int rows = array.GetUpperBound(0) - array.GetLowerBound(0) + 1;
            int cols = array.GetUpperBound(1) - array.GetLowerBound(1) + 1;

            double[,] result = new double[rows, cols];

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    result[i, j] = (double)array[i, j];
                }
            }

            return result;
        }

        protected static decimal[,] DoublesToDecimals(double[,] array)
        {
            int rows = array.GetUpperBound(0) - array.GetLowerBound(0) + 1;
            int cols = array.GetUpperBound(1) - array.GetLowerBound(1) + 1;

            decimal[,] result = new decimal[rows, cols];

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    result[i, j] = (decimal)array[i, j];
                }
            }

            return result;
        }

        public int Rows { get; protected set; }

        public int Columns { get; protected set; }

        public int[] Shape { get { return new int[2] { Rows, Columns }; } }

        public NMatrix(decimal[,] data)
        {
            Data = data;

            Rows = Data.GetUpperBound(0) - Data.GetLowerBound(0) + 1;
            Columns = Data.GetUpperBound(1) - Data.GetLowerBound(1) + 1;
        }

        public NMatrix(double[,] data)
        {
            Data = DoublesToDecimals(data);

            Rows = Data.GetUpperBound(0) - Data.GetLowerBound(0) + 1;
            Columns = Data.GetUpperBound(1) - Data.GetLowerBound(1) + 1;
        }

        public static NMatrix I(int size)
        {
            decimal[,] data = new decimal[size, size];
            for (int i = 0; i < size; i++)
            {
                for (int j = 0; j < size; j++)
                {
                    if (i == j)
                    {
                        data[i, j] = 1;
                    }
                    else
                    {
                        data[i, j] = 0;
                    }
                }
            }

            return new NMatrix(data);
        }

        public NMatrix I()
        {
            return I(this.Columns);
        }

        public IMatrix Identity()
        {
            return I(this.Columns);
        }

        public NMatrix T()
        {
            decimal[,] newData = new decimal[Columns, Rows];

            for (int i = 0; i < Rows; i++)
            {
                for (int j = 0; j < Columns; j++)
                {
                    newData[j, i] = Data[i, j];
                }
            }

            return new NMatrix(newData);
        }

        public IMatrix Transpose()
        {
            return this.T();
        }

        public static NMatrix Minors(NMatrix matrix)
        {
            NMatrix minors = new NMatrix(new decimal[matrix.Rows, matrix.Columns]);

            for (int i = 0; i < matrix.Rows; i++)
            {
                for (int j = 0; j < matrix.Columns; j++)
                {
                    if (matrix.Rows - 1 > 0 && matrix.Columns - 1 > 0)
                    {
                        NMatrix minorCalc = new NMatrix(new decimal[matrix.Rows - 1, matrix.Columns - 1]);

                        int x0 = 0;
                        for (int x = 0; x < matrix.Rows; x++)
                        {
                            if (x == i)
                            {
                                x++;
                            }
                            if (x == matrix.Rows)
                            {
                                break;
                            }

                            int y0 = 0;
                            for (int y = 0; y < matrix.Columns; y++)
                            {
                                if (y == j)
                                {
                                    y++;
                                }
                                if (y == matrix.Columns)
                                {
                                    break;
                                }

                                minorCalc.Data[x0, y0] = matrix.Data[x, y];
                                
                                y0++;
                            }
                            x0++;
                        }


                        minors.Data[i, j] = NMatrix.Determinant(minorCalc);
                    }
                    else if (matrix.Rows == 1 && matrix.Columns == 1)
                    {
                        minors.Data[i, j] = matrix.Data[i, j];
                    }
                    else
                    {
                        throw new ArgumentException("A minor can only be calculated for a square matrix.");
                    }
                }
            }

            return minors;
        }

        public NMatrix Minors()
        {
            return NMatrix.Minors(this);
        }

        public IMatrix MinorsMatrix()
        {
            return NMatrix.Minors(this);
        }

        public static NMatrix Cofactors(NMatrix matrix)
        {
            NMatrix minors = NMatrix.Minors(matrix);

            for (int i = 0; i < matrix.Rows; i++)
            {
                for (int j = 0; j < matrix.Columns; j++)
                {
                    minors.Data[i, j] *= (Tools.Validators.IsEven(i + j)) ? 1 : -1;
                }
            }

            return minors;// Now holds cofactors
        }

        public NMatrix Cofactors()
        {
            return NMatrix.Cofactors(this);
        }

        public IMatrix CofactorsMatrix()
        {
            return NMatrix.Cofactors(this);
        }

        public static decimal Determinant(NMatrix matrix)
        {
            if (matrix.Rows != matrix.Columns)
            {
                throw new ArgumentException("Determinant calculation failed - the matrix wasn't square.");
            }

            decimal result = 0;
            if (matrix.Rows == 0)
            {

            }
            else if (matrix.Rows == 1)
            {
                result = matrix.Data[0, 0];
            }
            else
            {
                NMatrix cfs;
                try
                {
                    cfs = NMatrix.Cofactors(matrix);
                }
                catch (ArgumentException)
                {
                    // IS THIS CORRECT?!
                    throw new ArgumentException("Determinant calculation failed - this was likely because its determinant was undifined.");
                }

                for (int i = 0; i < matrix.Columns; i++)
                {
                    result += matrix.Data[0, i] * cfs.Data[0, i];
                }
            }

            return result;
        }

        public decimal Determinant()
        {
            return NMatrix.Determinant(this);
        }

        public static NMatrix Adjoint(NMatrix matrix)
        {
            return matrix.Cofactors().T();
        }

        public NMatrix Adjoint()
        {
            return NMatrix.Adjoint(this);
        }

        public IMatrix AdjointMatrix()
        {
            return NMatrix.Adjoint(this);
        }

        public static NMatrix operator +(NMatrix a, NMatrix b)
        {
            decimal[,] newData = new decimal[a.Rows, a.Columns];

            for (int i = 0; i < a.Rows; i++)
            {
                for (int j = 0; j < a.Columns; j++)
                {
                    newData[i, j] = a.Data[i, j] + b.Data[i, j];
                }
            }

            return new NMatrix(newData);
        }

        public static NMatrix operator +(NMatrix a, decimal b)
        {
            return a + (a.I() * b);
        }

        public static NMatrix operator +(decimal a, NMatrix b)
        {
            return (b.I() * a) + b;
        }

        public void Add(IMatrix matrix)
        {
            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    this.Data[i, j] = this.Data[i, j] + matrix[i, j];
                }
            }
        }

        public void Add(decimal value)
        {
            this.Add(this.I() * value);
        }

        public static NMatrix operator -(NMatrix a, NMatrix b)
        {
            decimal[,] newData = new decimal[a.Rows, a.Columns];

            for (int i = 0; i < a.Rows; i++)
            {
                for (int j = 0; j < a.Columns; j++)
                {
                    newData[i, j] = a.Data[i, j] - b.Data[i, j];
                }
            }

            return new NMatrix(newData);
        }

        public static NMatrix operator -(NMatrix a, decimal b)
        {
            return a - (a.I() * b);
        }

        public static NMatrix operator -(decimal a, NMatrix b)
        {
            return (b.I() * a) - b;
        }

        public void Subtract(IMatrix matrix)
        {
            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    this.Data[i, j] = this.Data[i, j] - matrix[i, j];
                }
            }
        }

        public void Subtract(decimal value)
        {
            this.Subtract(this.I() * value);
        }

        public static NMatrix operator *(NMatrix a, NMatrix b)
        {
            decimal[,] newData = new decimal[a.Rows, b.Columns];

            for (int x = 0; x < a.Rows; x++)
            {
                for (int y= 0; y < b.Columns; y++)
                {
                    newData[x, y] = 0;

                    for (int i = 0; i < a.Columns; i++)
                    {
                        newData[x, y] += a.Data[x, i] * b.Data[i, y];
                    }
                }
            }

            return new NMatrix(newData);
        }

        public static NMatrix operator *(NMatrix a, decimal b)
        {
            decimal[,] newData = new decimal[a.Rows, a.Columns];

            for (int i = 0; i < a.Rows; i++)
            {
                for (int j = 0; j < a.Columns; j++)
                {
                    newData[i, j] = a.Data[i, j] * b;
                }
            }

            return new NMatrix(newData);
        }

        public static NMatrix operator *(decimal a, NMatrix b)
        {
            decimal[,] newData = new decimal[b.Rows, b.Columns];

            for (int i = 0; i < b.Rows; i++)
            {
                for (int j = 0; j < b.Columns; j++)
                {
                    newData[i, j] = a * b.Data[i, j];
                }
            }

            return new NMatrix(newData);
        }

        public void Multiply(IMatrix matrix)
        {
            decimal[,] newData = new decimal[this.Rows, matrix.Columns];

            for (int x = 0; x < this.Rows; x++)
            {
                for (int y = 0; y < matrix.Columns; y++)
                {
                    newData[x, y] = 0;

                    for (int i = 0; i < this.Columns; i++)
                    {
                        newData[x, y] += this.Data[x, i] * matrix[i, y];
                    }
                }
            }

            this.Data = newData;
        }

        public void Multiply(decimal value)
        {
            this.Multiply(this.I() * value);
        }

        public static NMatrix operator /(NMatrix a, NMatrix b)
        {
            // Undifined exeption


            return a * (b.Adjoint() / b.Determinant());
        }

        public static NMatrix operator /(NMatrix a, decimal b)
        {
            // DivideByZeroExeption


            return a * (1 / b);
        }

        public static NMatrix operator /(decimal a, NMatrix b)
        {
            // Undifined exeption



            return a * (b.Adjoint() / b.Determinant());
        }

        public void Divide(IMatrix matrix)
        {
            IMatrix adjoint = matrix.AdjointMatrix();
            adjoint.Multiply(1 / matrix.Determinant());

            this.Multiply(adjoint);
        }

        public void Divide(decimal value)
        {
            this.Multiply(1 / value);
        }

        public virtual bool EqualsPrecision(object o, int precision = 24)
        {
            bool result = false;

            if (o is IMatrix)
            {
                if (((IMatrix)o).Rows == this.Rows && ((IMatrix)o).Columns == this.Columns)
                {
                    result = true;
                    for (int i = 0; i < this.Rows; i++)
                    {
                        for (int j = 0; j < this.Columns; j++)
                        {
                            if (Math.Round(this.Data[i, j], precision) != Math.Round(((IMatrix)o)[i, j], precision))
                            {
                                result = false;
                                break;
                            }
                        }
                    }
                }
            }
            else if (o is decimal[,])
            {
                if (((decimal[,])o).GetUpperBound(0) - ((decimal[,])o).GetUpperBound(0) == this.Rows && ((decimal[,])o).GetUpperBound(1) - ((decimal[,])o).GetUpperBound(1) == this.Columns)
                {
                    result = true;
                    for (int i = 0; i < this.Rows; i++)
                    {
                        for (int j = 0; j < this.Columns; j++)
                        {
                            if (Math.Round(this.Data[i, j], precision) != Math.Round(((decimal[,])o)[i, j], precision))
                            {
                                result = false;
                                break;
                            }
                        }
                    }
                }
            }

            return result;
        }
        
        public override bool Equals(object o)
        {
            return this.EqualsPrecision(o, 12);
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        public static bool operator ==(NMatrix a, NMatrix b)
        {
            return a.Equals(b);
        }

        public static bool operator !=(NMatrix a, NMatrix b)
        {
            return !a.Equals(b);
        }

        public decimal this[int row, int col] { get { return Data[row, col]; } }

        public static explicit operator decimal[,](NMatrix matrix)
        {
            return matrix.Data;
        }

        public static explicit operator double[,] (NMatrix matrix)
        {
            return DecimalsToDoubles(matrix.Data);
        }

        public static explicit operator string (NMatrix matrix)
        {
            return matrix.ToString();
        }

        public static decimal Dot(IMatrix a, IMatrix b)
        {
            if (a.Rows != b.Rows || a.Columns != b.Columns)
            {
                throw new ArgumentException("Matrix Dot failed - matraces had different shapes.");
            }

            decimal result = 0;

            for (int i = 0; i < a.Rows; i++)
            {
                for (int j = 0; j < a.Columns; j++)
                {
                    result += a[i, j] * b[i, j];
                }
            }

            return result;
        }

        public decimal Dot(IMatrix matrix)
        {
            return Dot(this, matrix);
        }

        new public string ToString()
        {
            double[,] newData = DecimalsToDoubles(this.Data);

            string result = "";
            for (int i = 0; i < this.Rows; i++)
            {
                for (int j = 0; j < this.Columns; j++)
                {
                    result += Convert.ToString(newData[i, j]) + ((j == this.Columns - 1) ? ((i == this.Rows - 1) ? "" : "\n") : " ");
                }
            }

            return result;
        }

        new public string ToStringWithBrackets()
        {
            double[,] newData = DecimalsToDoubles(this.Data);

            string result = "";

            //result += "_";
            //for (int i = 0; i < this.Columns; i++) { result += " "; }
            //result += "_\n";

            for (int i = 0; i < this.Rows; i++)
            {
                result += "|";
                for (int j = 0; j < this.Columns; j++)
                {
                    result += Convert.ToString(newData[i, j]) + ((j == this.Columns - 1) ? "" : " ");
                }
                result += "|" + "\n";
            }

            //result += "-";
            //for (int i = 0; i < this.Columns; i++) { result += " "; }
            //result += "-\n";

            return result;
        }
    }
}