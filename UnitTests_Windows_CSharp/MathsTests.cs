using Microsoft.VisualStudio.TestTools.UnitTesting;

using QuasarCode.Library.Maths;
using QuasarCode.Library.Maths.Matrices;
using QuasarCode.Library.Maths.Matrices.Vectors;
using QuasarCode.Library.Maths.Units;
using QuasarCode.Library.Maths.Units.Common;

namespace UnitTests_Windows_CSharp
{
    [TestClass]
    public class MathsTests
    {
        [TestMethod]
        public void Test1()
        {
            IMatrix<double> mat = new NMatrix(new double[,] { { 1, 2, 3 },
                                                              { 4, 5, 6 },
                                                              { 7, 8, 9 } });

            //IMatrix<double> mat2 = mat.Multiply(IdentityMatrix.CreateNew(3));
            IMatrix<double> mat2 = mat.Multiply(mat);

            IMatrix<double> mat3 = mat2.Add(10);

            System.Console.WriteLine(mat);
            System.Console.WriteLine();
            System.Console.WriteLine(mat2);
            System.Console.WriteLine();
            System.Console.WriteLine(mat3);
        }

        [TestMethod]
        public void Test2()
        {
            IMatrix<double> mat = new NMatrix(new double[,] { { 1 },
                                                              { 4 },
                                                              { 7 },
                                                              { 10 }});
            System.Console.WriteLine(mat);
        }
    }
}
