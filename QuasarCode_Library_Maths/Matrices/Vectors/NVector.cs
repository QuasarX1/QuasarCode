using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public sealed class NVector : Vector<double>
    {
        //public NVector NewVector(double[,] data, bool enableCasching = true)
        //{
        //    return;
        //}

        public NVector(double[,] data, bool enableCasching = true) : base(data, (double a, double b) => a + b, (double a, double b) => a - b, (double a, double b) => a * b, (double a, double b) => a / b, (double a, double b) => a * b, enableCasching) { }

        public NVector(IVector<double> vector, bool enableCasching = true) : base(vector, enableCasching) { }
    }
}
