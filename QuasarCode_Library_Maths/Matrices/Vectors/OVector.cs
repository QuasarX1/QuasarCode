using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public sealed class OVector : Vector<object>
    {
        public OVector(object[,] data, bool enableCasching = true) : base(data, (object a, object b) => a + (dynamic)b, (object a, object b) => a - (dynamic)b, (object a, object b) => a * (dynamic)b, (object a, object b) => a / (dynamic)b, (object a, double b) => (dynamic)a * b, enableCasching) { }

        public OVector(IVector<object> vector, bool enableCasching = true) : base(vector, enableCasching) { }
    }
}
