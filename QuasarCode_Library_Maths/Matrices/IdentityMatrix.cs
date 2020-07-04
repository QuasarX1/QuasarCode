using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices
{
    /// <summary>
    /// Identity Matrix
    /// </summary>
    public sealed class IdentityMatrix : Matrix<double>
    {
        private IdentityMatrix(double[,] data, bool enableCasching = true) : base(data, (double a, double b) => a + b, (double a, double b) => a - b, (double a, double b) => a * b, (double a, double b) => a / b, (double a, double b) => a * b, enableCasching) { }

        public static IdentityMatrix CreateNew(int rank, bool enableCasching = false)
        {
            double[,] data = new double[rank, rank];

            for (int i = 0; i < rank; i++)
            {
                for (int j = 0; j < rank; j++)
                {
                    data[i, j] = (i != j) ? 0 : 1;
                }
            }

            return new IdentityMatrix(data, enableCasching);
        }
    }
}
