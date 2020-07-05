using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices
{
    /// <summary>
    /// Object Matrix - a matrix of generic objects
    /// </summary>
    public sealed class OMatrix : Matrix<object>
    {
        public OMatrix(object[,] data, bool enableCasching = true) : base(data, (object a, object b) => a + (dynamic)b, (object a, object b) => a - (dynamic)b, (object a, object b) => a * (dynamic)b, (object a, object b) => a / (dynamic)b, (object a, double b) => (dynamic)a * b, enableCasching) { }

        public OMatrix(IMatrix<object> matrix, bool enableCasching = true) : base(matrix, enableCasching) { }
    }
}
