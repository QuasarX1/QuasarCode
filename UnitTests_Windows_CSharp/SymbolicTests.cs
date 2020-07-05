using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.Collections.Generic;

using QuasarCode.Library.Symbolic;
using static QuasarCode.Library.Symbolic.Constant;

namespace UnitTests_Windows_CSharp
{
    [TestClass]
    public class SymbolicTests
    {
        [TestMethod]
        public void Test()
        {
            Dictionary<string, Variable> variables = Equasion.CreateVariables(new string[] { "a", "b", "c" },
                                                                              new decimal[] { 1, 1, 0 });

            Constant pi = Constant.PI;
            Variable x = new Variable("x");

            //Equasion quad = new Equasion(variables["a"] * x ^ 2 + variables["b"] * x + variables["c"], 0);
            //System.Console.WriteLine(quad);
            //quad.SolveFor(x);

            //System.Console.WriteLine(x);

            Variable test = variables["a"];
            test.sin();
            test.ToString();

            //System.Console.WriteLine(test);
        }
    }
}
