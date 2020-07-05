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
        public VMatrix(IValue[,] data, bool enableCasching = true) : base(data, (IValue a, IValue b) => a.Add(b), (IValue a, IValue b) => a.Sub(b), (IValue a, IValue b) => a.Mult(b), (IValue a, IValue b) => a.Div(b), (IValue a, double b) => a.Mult(b), enableCasching) { }

        public VMatrix(IMatrix<IValue> matrix, bool enableCasching = true) : base(matrix, enableCasching) { }
    }
}
