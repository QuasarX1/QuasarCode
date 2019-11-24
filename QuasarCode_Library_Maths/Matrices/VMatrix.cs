using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units;

namespace QuasarCode.Library.Maths.Matrices
{
    /// <summary>
    /// Value Matrix - a matrix of IValue objects.
    /// See QuasarCode.Library.Maths.Units.IValue
    /// </summary>
    public sealed class VMatrix : Matrix<IValue>
    {
        public VMatrix(IValue[,] data, bool enableCasching = true) : base(data, enableCasching) { }

        public VMatrix(IMatrix<IValue> matrix, bool enableCasching = true) : base(matrix, enableCasching) { }
    }
}
