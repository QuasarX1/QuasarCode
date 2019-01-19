using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using QuasarCode;
using static QuasarCode.Library.IO.Text.Console;

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

            int convert(string input)
            {
                return Convert.ToInt16(input);
            }

            Input("Numerical input wanted:", new Func<string, int>(convert));
        }

        [TestMethod]
        public void Option_Test()
        {
            string[] choices = new string[] { "Option A", "Option B", "Option C", "Option D", "Option E", "Option F", "Option G", "Option H", "Option I", "Option J", "Option K", "Option L" };

            Option(choices, "Select an option:");

            Option<string>(choices, "Select an option:");
        }
    }
}
