using System;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using QuasarCode;
using static QuasarCode.Library.IO.Text.Console;
using static QuasarCode.Library.Tools.Validators;
using QuasarCode.Library.Tools;

namespace UnitTests_Windows
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void Print_Test()
        {
            Print();
            Print("Test print");
            Print("Test print 2", end: "    ");
            Print("Hi", "Chris. This is the ", 3, "rd test.");
        }

        // DO NOT RUN - requires input
        [TestMethod]
        public void Input_Test()
        {
            Input();
            Input("Input required:");
            Input("More input required", " -> ");

            Input("Numerical input wanted:", new Func<object, bool>(IsInt), "The input wasn't an integer.");

            int convert(string input)
            {
                return Convert.ToInt16(input);
            }

            Input("Numerical input wanted:", new Func<string, int>(convert));
            //Input("Numerical input wanted:", new Func<object, bool>(IsInt), "The input wasn't an integer.", new Func<string, int>(convert));
            Input<int>("Numerical input wanted:", new Func<string, int>(convert), new Func<object, bool>(IsInt), "The input wasn't an integer.");
        }

        // DO NOT RUN - requires input
        [TestMethod]
        public void Option_Test()
        {
            string[] choices = new string[] { "Option A", "Option B", "Option C", "Option D", "Option E", "Option F", "Option G", "Option H", "Option I", "Option J", "Option K", "Option L" };

            Option(choices, "Select an option:");

            Option<string>(choices, "Select an option:");
        }

        [TestMethod]
        public void Validator_Test()
        {
            // IsAlpha
            Assert.AreEqual(IsAlpha('a'), true);
            Assert.AreEqual(IsAlpha("a"), true);
            Assert.AreEqual(IsAlpha("abc"), true);
            Assert.AreEqual(IsAlpha((object)'a'), true);
            Assert.AreEqual(IsAlpha((object)"abc"), true);
            
            Assert.AreEqual(IsAlpha('1'), false);
            Assert.AreEqual(IsAlpha("1"), false);
            Assert.AreEqual(IsAlpha("a1c"), false);
            Assert.AreEqual(IsAlpha((object)'1'), false);
            Assert.AreEqual(IsAlpha((object)"a1c"), false);

            // IsBool
            Assert.AreEqual(IsBool(true), true);
            Assert.AreEqual(IsBool(false), true);

            Assert.AreEqual(IsBool("Not bool"), false);

            // IsChar
            Assert.AreEqual(IsChar('a'), true);
            Assert.AreEqual(IsChar("a"), true);

            Assert.AreEqual(IsChar("abc"), false);
            Assert.AreEqual(IsChar(10), false);

            // IsDouble
            Assert.AreEqual(IsDouble(1.1), true);
            Assert.AreEqual(IsDouble(1), true);
            Assert.AreEqual(IsDouble("0.5"), true);

            Assert.AreEqual(IsDouble("Not double"), false);

            // IsInt
            Assert.AreEqual(IsInt(10), true);
            Assert.AreEqual(IsInt("100"), true);
            Assert.AreEqual(IsInt('5'), true);

            Assert.AreEqual(IsInt(0.1), false);
            Assert.AreEqual(IsInt("8.3"), false);
            Assert.AreEqual(IsInt("Not an integer"), false);

            // IsString
            Assert.AreEqual(IsString("A string"), true);
            Assert.AreEqual(IsString('a'), true);
            Assert.AreEqual(IsString(5), true);
        }

        [TestMethod]
        public void Range_Test()
        {
            Assert.AreEqual(InRange(50, 0, 100), true);
            Assert.AreEqual(InRange(-1, 0, 100), false);
            Assert.AreEqual(InRange(0, 0, 100), true);
            Assert.AreEqual(InRange(1, 0, 100), true);
            Assert.AreEqual(InRange(99, 0, 100), true);
            Assert.AreEqual(InRange(100, 0, 100), false);
            Assert.AreEqual(InRange(101, 0, 100), false);


            Assert.AreEqual(InRange(50, 0, 100, inside: false), false);
            Assert.AreEqual(InRange(-1, 0, 100, inside: false), true);
            Assert.AreEqual(InRange(0, 0, 100, inside: false), false);
            Assert.AreEqual(InRange(1, 0, 100, inside: false), false);
            Assert.AreEqual(InRange(99, 0, 100, inside: false), false);
            Assert.AreEqual(InRange(100, 0, 100, inside: false), true);
            Assert.AreEqual(InRange(101, 0, 100, inside: false), true);
        }

        [TestMethod]
        public void Even_Test()
        {
            Assert.AreEqual(IsEven(0), true);
            Assert.AreEqual(IsEven(1), false);
            Assert.AreEqual(IsEven(2), true);

            Assert.AreEqual(IsEven(0.0), true);
            Assert.AreEqual(IsEven(1.0), false);
            Assert.AreEqual(IsEven(2.0), true);

            Assert.AreEqual(IsEven(0.5), true);
            Assert.AreEqual(IsEven(1.4), false);
            Assert.AreEqual(IsEven(1.5), true);// Conversion to integer rounds to nearest int
            Assert.AreEqual(IsEven(2.5), true);
        }

        [TestMethod]
        public void MultiItterator_Test()
        {
            foreach (Tuple<int, object[]> items in new MultiItterator(new object[] { 1, 2, 3 }, new string[] { "a", "b", "c" }, new object[] { false, true, false }))
            {
                Assert.AreEqual(items.Item1, (int)items.Item2[0] - 1);
                Assert.AreEqual(IsEven(items.Item2[0]), (bool)items.Item2[2]);
            }


            int[] result1 = new int[] { 3, 2, 4 };
            int[] result2 = new int[] { 1, 5, 3 };
            int[] result3 = new int[] { 4, 2, 5 };

            int[] averages = new int[] { 0, 0, 0 };
            foreach (Tuple<int, int[]> items in new MultiItterator<int>(result1, result2, result3))
            {
                averages[items.Item1] = (items.Item2[0] + items.Item2[1] + items.Item2[2]) / 3;
            }
            
            Assert.AreEqual(averages[0], 2);// Truncates float
            Assert.AreEqual(averages[1], 3);
            Assert.AreEqual(averages[2], 4);
        }
    }
}
