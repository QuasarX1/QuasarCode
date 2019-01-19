using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using QuasarCode;
using static QuasarCode.Library.IO.Text.Console;
using static QuasarCode.Library.Tools.Validators;

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
            Assert.AreEqual(IsChar("a"), true);// ?????

            Assert.AreEqual(IsChar(1), false);

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

            Assert.AreEqual(IsString(5), false);
        }
    }
}
