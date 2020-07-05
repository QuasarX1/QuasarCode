using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units;
using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public sealed class VVector : Vector<IValue>
    {
        public VVector(IValue[,] data, bool enableCasching = true) : base(data, (IValue a, IValue b) => a.Add(b), (IValue a, IValue b) => a.Sub(b), (IValue a, IValue b) => a.Mult(b), (IValue a, IValue b) => a.Div(b), (IValue a, double b) => a.Mult(b), enableCasching) { }

        public VVector(IVector<IValue> vector, bool enableCasching = true) : base(vector, enableCasching) { }
    }
}
