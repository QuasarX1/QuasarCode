using System;
using System.Collections.Generic;
using System.Text;

using QuasarCode.Library.Maths.Units;
using QuasarCode.Library.Maths.Units.Common;

namespace QuasarCode.Library.Maths.Matrices.Vectors
{
    public interface IVector : IMatrix
    {
        IUnit Unit { get; }
        bool ColumnFormat { get; }
        double this[int index] { get; }

        double[,] GetVectorData();

        new IVector Transpose();

        double ScalarProduct(IVector vector);

        double VectorProduct(IVector vector);

        IVector Add(IVector matrix);

        IVector Subtract(IVector matrix);

        IVector Multiply(IVector matrix);//TODO: HOW?!

        IVector Divide(IVector matrix);//TODO: HOW?!
    }
}