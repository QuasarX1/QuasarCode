using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices
{
    /// <summary>
    /// Number Matrix - a matrix of doubles
    /// </summary>
    public sealed class NMatrix : Matrix<double>
    {
        public NMatrix(double[,] data, bool enableCasching = true) : base(data, enableCasching) { }

        public NMatrix(IMatrix<double> matrix, bool enableCasching = true) : base(matrix, enableCasching) { }
    }
}
