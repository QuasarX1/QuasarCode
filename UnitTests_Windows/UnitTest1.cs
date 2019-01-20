using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using QuasarCode;
using static QuasarCode.Library.IO.Text.Console;
using static QuasarCode.Library.Tools.Validators;
using QuasarCode.Library.Tools;
using QuasarCode.Library.Games.Spinners;
using QuasarCode.Library.Games.Dice;

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

        [TestMethod]
        public void Spinner_Test()
        {
            string[] backup = new string[] { "Red", "Blue", "Yellow", "Green" };
            Spinner<string> spinner = new Spinner<string>("Red", "Blue", "Yellow", "Green");

            Tuple<int, string> result;
            for (int i = 0; i < 20; i++)
            {
                result = spinner.ContextSpin();
                Assert.AreEqual(result.Item2, backup[result.Item1]);
            }
        }

        [TestMethod]
        public void Dice_Test()
        {
            NDice dice = new NDice(6);

            for (int i = 0; i < 20; i++)
            {
                Assert.AreEqual(InRange(dice.Roll(), 1, 7), true);
            }

            dice = new Dice6();

            for (int i = 0; i < 20; i++)
            {
                Assert.AreEqual(InRange(dice.Roll(), 1, 7), true);
            }

            dice = new Dice8();

            for (int i = 0; i < 20; i++)
            {
                Assert.AreEqual(InRange(dice.Roll(), 1, 9), true);
            }

            dice = new Dice12();

            for (int i = 0; i < 20; i++)
            {
                Assert.AreEqual(InRange(dice.Roll(), 1, 13), true);
            }


            DiceCup cup = new DiceCup(6, 2);

            int[] results;
            for (int i = 0; i < 20; i++)
            {
                results = cup.Roll();

                foreach (int result in results)
                {
                    Assert.AreEqual(InRange(result, 1, 7), true);
                }

                Assert.AreEqual(InRange(results.Sum(), 2, 13), true);
            }


            DynamicDiceCup dynamicCup = new DynamicDiceCup();

            dynamicCup += new Dice12();
            dynamicCup.PushDice(new Dice6());


            for (int i = 0; i < 20; i++)
            {
                results = dynamicCup.Roll();

                Assert.AreEqual(InRange(results[0], 1, 13), true);
                Assert.AreEqual(InRange(results[1], 1, 7), true);

                Assert.AreEqual(InRange(results.Sum(), 2, 19), true);
            }

            dynamicCup--;

            Assert.AreEqual(dynamicCup.Count, 1);

            Assert.AreEqual(dynamicCup.PopDice().GetType(), typeof(Dice12));

            Assert.AreEqual(dynamicCup.Count, 0);

            try
            {
                dynamicCup.Roll();
                throw new Exception("Roll() didn't throw an exception. It should have been empty.");
            }
            catch (InvalidOperationException) { }
        }
    }
}
