﻿using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using QuasarCode;
using static QuasarCode.Library.IO.Text.Console;
using static QuasarCode.Library.Tools.Validators;
using QuasarCode.Library.Tools;
using QuasarCode.Library.Games.Spinners;
using QuasarCode.Library.Games.Dice;
using QuasarCode.Library.Games.Cards;
using QuasarCode.Library.Maths;
using QuasarCode.Library.Maths.Matrices;
using QuasarCode.Library.Maths.Matrices.Vectors;
using QuasarCode.Library.Maths.Coordinates;
using QuasarCode.Library.Maths.Coordinates._1D;
using QuasarCode.Library.Maths.Coordinates._2D;
using QuasarCode.Library.Maths.Coordinates._3D;
using QuasarCode.Library.Maths.Coordinates.ND;
using QuasarCode.Library.Maths.Coordinates.Systems;
using QuasarCode.Library.Maths.Coordinates.Systems._1D;
using QuasarCode.Library.Maths.Coordinates.Systems._2D;
using QuasarCode.Library.Maths.Coordinates.Systems._3D;
using QuasarCode.Library.Maths.Coordinates.Systems.ND;
using QuasarCode.Library.Maths.Fields;
using QuasarCode.Library.Symbolic;

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

        [TestMethod]
        public void Cards_Test()
        {
            Deck deck = new Deck("Deck", 2);

            Assert.AreEqual(54, deck.Cards.Length);
            Assert.AreEqual(deck.Cards.Length, deck.Count);

            CardGroup<PlayingCard> hand1 = new CardGroup<PlayingCard>("Hand1");
            CardGroup<PlayingCard> hand2 = new CardGroup<PlayingCard>("Hand2");
            CardGroup<PlayingCard> hand3 = new CardGroup<PlayingCard>("Hand3");

            CardGroup<PlayingCard> spare1 = new CardGroup<PlayingCard>("Spare1");
            CardGroup<PlayingCard> spare2 = new CardGroup<PlayingCard>("Spare2");
            CardGroup<PlayingCard> spare3 = new CardGroup<PlayingCard>("Spare3");

            CardGroup<PlayingCard>[] hands = new CardGroup<PlayingCard>[] { hand1, hand2, hand3 };
            List<CardGroup<PlayingCard>> handsList = new List<CardGroup<PlayingCard>> { hand1, hand2, hand3 };

            CardGroup<PlayingCard>[] spares = new CardGroup<PlayingCard>[] { spare1, spare2, spare3 };
            List<CardGroup<PlayingCard>> sparesList = new List<CardGroup<PlayingCard>> { spare1, spare2, spare3 };

            deck.InitialiseGroup(new CardGroup<PlayingCard>[] { hand1, hand2, hand3, spare1, spare2, spare3 });

            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(hand1, hand2, hand3);

            foreach (CardGroup<PlayingCard> hand in hands)
            {
                Assert.AreEqual(18, hand.Count);
            }

            deck.Reset();

            Assert.AreEqual(0, hand1.Count);
            Assert.AreEqual(0, hand2.Count);
            Assert.AreEqual(0, hand3.Count);
            Assert.AreEqual(0, spare1.Count);
            Assert.AreEqual(0, spare2.Count);
            Assert.AreEqual(0, spare3.Count);


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(hands);

            foreach (CardGroup<PlayingCard> hand in hands)
            {
                Assert.AreEqual(18, hand.Count);
            }

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(handsList);

            foreach (CardGroup<PlayingCard> hand in handsList)
            {
                Assert.AreEqual(18, hand.Count);
            }

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(hands, 7);

            foreach (CardGroup<PlayingCard> hand in hands)
            {
                Assert.AreEqual(7, hand.Count);
            }

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(handsList, 7);

            foreach (CardGroup<PlayingCard> hand in handsList)
            {
                Assert.AreEqual(7, hand.Count);
            }

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(hands, 7, spare1);

            foreach (CardGroup<PlayingCard> hand in hands)
            {
                Assert.AreEqual(7, hand.Count);
            }

            Assert.AreEqual(33, spare1.Count);

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(handsList, 7, spare1);

            foreach (CardGroup<PlayingCard> hand in handsList)
            {
                Assert.AreEqual(7, hand.Count);
            }

            Assert.AreEqual(33, spare1.Count);

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(hands, 7, spares);

            foreach (CardGroup<PlayingCard> hand in hands)
            {
                Assert.AreEqual(7, hand.Count);
            }

            foreach (CardGroup<PlayingCard> hand in spares)
            {
                Assert.AreEqual(11, hand.Count);
            }

            deck.Reset();


            deck.Shuffle();

            deck.Deal<CardGroup<PlayingCard>>(handsList, 7, sparesList);

            foreach (CardGroup<PlayingCard> hand in handsList)
            {
                Assert.AreEqual(7, hand.Count);
            }

            foreach (CardGroup<PlayingCard> hand in sparesList)
            {
                Assert.AreEqual(11, hand.Count);
            }

            deck.Reset();

            deck.ReleaseGroup(new CardGroup<PlayingCard>[] { hand1, hand2, hand3, spare1, spare2, spare3 });


            Deck newDeck = new Deck("Deck", 0);

            CardGroup<PlayingCard> gameHand1 = new CardGroup<PlayingCard>("Hand1");
            CardGroup<PlayingCard> gameHand2 = new CardGroup<PlayingCard>("Hand2");
            CardStack<PlayingCard> drawPile = new CardStack<PlayingCard>("Draw Pile");

            newDeck.InitialiseGroup(gameHand1, gameHand2, drawPile);

            newDeck.Deal<ICardGroup<PlayingCard>>(new CardGroup<PlayingCard>[] { gameHand1, gameHand2 }, 7, drawPile, false);

            newDeck.ReleaseGroup(gameHand1, gameHand2);// These still have cards

            newDeck.Reset();

            Assert.AreEqual(7, gameHand1.Count);// Hand hasn't returned cards!
            Assert.AreEqual(7, gameHand2.Count);// Hand hasn't returned cards!
            Assert.AreEqual(0, drawPile.Count);

            Assert.AreEqual(52, newDeck.Count);// All cards appear to have been returned but hands still reference some!
        }

        [TestMethod]
        public void UnitsAndValues_Test()
        {
            Value length = new Value(10.25, Units.m);
            StandardValue stdLength = length.ToStandardValue();

            Assert.AreEqual(length.Magnitude, stdLength.Magnitude * Math.Pow(10, stdLength.StandardPower));
            Assert.AreEqual(length.Unit, stdLength.Unit);

            Value revertedLength = stdLength.ToValue();

            Assert.AreEqual(length.Magnitude, revertedLength.Magnitude);
            Assert.AreEqual(length.Unit, revertedLength.Unit);


            CompoundUnit KgPERm3 = new CompoundUnit(new Tuple<Units, int>(Units.Kg, 1), new Tuple<Units, int>(Units.m, -3));

            Value density = new Value(1.0/8.0, KgPERm3);

            Value volume = new Value(8, Units.m, 3);

            Value mass = density * volume;

            Assert.AreEqual(1, mass.Magnitude);
            CompoundUnit massUnit = new CompoundUnit(new Tuple<Units, int>(Units.Kg, 1));
            Assert.AreEqual(true, massUnit == (CompoundUnit)mass.Unit);


            Value dist1 = new Value(2, Units.m);

            Value dist2 = new Value(1, Units.m);

            Value ratio = dist1 / dist2;

            Assert.AreEqual(2, ratio.Magnitude);

            CompoundUnit ratioUnit = new CompoundUnit(new Tuple<Units, int>(Units.NoUnit, 0));
            Assert.AreEqual(true, ratioUnit == (CompoundUnit)ratio.Unit);


            Value velocity = new Value(2, new CompoundUnit(new Tuple<Units, int>(Units.m, 1), new Tuple<Units, int>(Units.s, -1)));

            Value time = new Value(1, Units.s);

            StandardValue acc = (velocity / time).ToStandardValue();

            Assert.AreEqual(2, acc.Magnitude);
            CompoundUnit accUnit = new CompoundUnit(new Tuple<Units, int>(Units.m, 1), new Tuple<Units, int>(Units.s, -2));
            Assert.AreEqual(true, accUnit == (CompoundUnit)acc.Unit);

            Print(velocity + " / " + time + " = " + acc);
            Assert.AreEqual("2 m s\u02C9\u00B9 / 1 s = 2 m s\u02C9\u00B2", velocity + " / " + time + " = " + acc);
            
            
            StandardValue sValue = new StandardValue(10.23, new CompoundUnit(new Tuple<Units, int>(Units.km, 1), new Tuple<Units, int>(Units.h, -1)), 2);
            Print(sValue);
            Assert.AreEqual("1.023 x 10\u00B3 km h\u02C9\u00B9", sValue.ToString());


            Value r_1 = new Value(10, Units.m);
            Value r2_1 = r_1 ^ 2;
            Print(r2_1);


            StandardValue r_2 = new StandardValue(10, Units.m);
            StandardValue r2_2 = r_2 ^ 2;
            Print(r2_2);


            Value testConversion1 = new Value(1000, new Unit(Units.g));
            Value gInKg = (Value)testConversion1.As(Units.Kg);
            Print(gInKg.ToString() + " in " + testConversion1.ToString());
            Assert.AreEqual(1, gInKg.Magnitude);

            Value testConversion2 = new Value(1, new Unit(Units.g));
            StandardValue oxInGrams = ((Value)testConversion2.As(Units.oz)).ToStandardValue();
            Print(oxInGrams.ToString() + " in " + testConversion2.ToString());
            Assert.AreEqual(Math.Round(0.0352739619495804, 6, MidpointRounding.AwayFromZero), Math.Round(oxInGrams.GetMagnitude(), 6, MidpointRounding.AwayFromZero));

            StandardValue testConversion3 = new StandardValue(1, new CompoundUnit(new Unit(Units.m), new Unit(Units.km)));
            StandardValue m2Inmkm = ((Value)testConversion3.As(Units.m.Pow(2))).ToStandardValue();
            Print(m2Inmkm.ToString() + " in " + testConversion3.ToString());
            Assert.AreEqual(1000, m2Inmkm.GetMagnitude());

            StandardValue testConversion4 = new StandardValue(1, new CompoundUnit((Unit)Units.Kg, (Unit)Units.m, Units.s.Pow(-1)));
            StandardValue noncenceConversion = ((Value)testConversion4.As(new CompoundUnit((Unit)Units.lb, (Unit)Units.m, Units.s.Pow(-1)))).ToStandardValue();
            Print(noncenceConversion.Round(5).ToString() + " in " + testConversion4.ToString());

            Print(new Value(16, Units.oz) + " in " + new Value(16, Units.oz).As((Unit)Units.lb));
        }

        [TestMethod]
        public void Matraces_Test()
        {
            NMatrix matrix = new NMatrix(new decimal[2, 2] { { 1, 0 }, { 0, 1 } });

            Assert.AreEqual(1, matrix.Determinant());

            Assert.AreEqual(4, (matrix * 2).Determinant());

            NMatrix test = matrix.T();
            Assert.IsTrue(matrix == matrix.T());

            Assert.IsTrue(matrix == matrix.I());


            NMatrix A = new NMatrix(new double[2, 2] {
                { 2, 4 },
                { 7, 5 }
            });

            NMatrix A_T = A.T();

            Assert.AreEqual(new NMatrix(new double[2, 2] { { 2, 7 }, { 4, 5 } }), A_T);

            NMatrix A_I = A.I();

            NMatrix A_adjoint = A.Adjoint();

            NMatrix A_inverse = A_adjoint / A.Determinant();

            NMatrix A_result = A * A_inverse;

            Assert.AreEqual(A_I, A_result);


            NMatrix B = new NMatrix(new decimal[2, 2] {
                { 2, 4 },
                { 1, 5 }
            });

            NMatrix B_T = B.T();

            Assert.AreEqual(new NMatrix(new decimal[2, 2] { { 2, 1 }, { 4, 5 } }), B_T);

            NMatrix B_I = B.I();

            NMatrix B_adjoint = B.Adjoint();

            NMatrix B_inverse = B_adjoint / B.Determinant();

            NMatrix B_result = B * B_inverse;

            Assert.AreEqual(B_I, B_result);


            NMatrix C = new NMatrix(new double[3, 3] {
            { 13, 8, -12 },
            { 11, 20, 6 },
            { 3, -8, 15 }
            });

            NMatrix C_T = C.T();

            Assert.AreEqual(new NMatrix(new double[3, 3] { { 13, 11, 3 }, { 8, 20, -8 }, { -12, 6, 15 } }), C_T);

            NMatrix C_I = C.I();

            NMatrix C_adjoint = C.Adjoint();

            NMatrix C_inverse = C_adjoint / C.Determinant();

            NMatrix C_result = C * C_inverse;

            Assert.AreEqual(C_I, C_result);


            NMatrix D = new NMatrix(new double[3, 3] {
                { 255, -98, 11 },
                { 45, 67, 59 },
                { -15, 36, -20 }
            });
            Print(D.ToStringWithBrackets());

            NMatrix D_T = D.T();
            Print(D_T.ToStringWithBrackets());
            
            Assert.AreEqual(new NMatrix(new double[3, 3] { { 255, 45, -15 }, { -98, 67, 36 }, { 11, 59, -20 } }), D_T);

            NMatrix D_I = D.I();
            Print(D_I.ToStringWithBrackets());

            NMatrix D_adjoint = D.Adjoint();
            Print(D_adjoint.ToStringWithBrackets());

            NMatrix D_inverse = D_adjoint / D.Determinant();
            Print(D_inverse.ToStringWithBrackets());

            NMatrix D_result = D * D_inverse;
            Print(D_result.ToStringWithBrackets());
            
            Assert.AreEqual(D_I, D_result);
            Assert.IsFalse(D_I.EqualsPrecision(D_result, 24));
        }

        [TestMethod]
        public void Vectors_Test()
        {
            var spaceTime = new Cartesian_ND(Units.m, Units.m, Units.m, Units.s);

            var i = new CartesianVector<Cartesian_ND>(1, 0, 0, 0);// Instantaniously move 1 in x

            var j = new CartesianVector<Cartesian_ND>(0, 1, 0, 0);// Instantaniously move 1 in y

            var k = new CartesianVector<Cartesian_ND>(0, 0, 1, 0);// Instantaniously move 1 in z

            var t = new CartesianVector<Cartesian_ND>(0, 0, 0, 1);// Move 1 in t

            var it = i + t;// Move 1 in x in 1 t
            var jt = j + t;// Move 1 in y in 1 t
            var kt = k + t;// Move 1 in z in 1 t

            var loc = new Cartesian_ND_Coordinate(spaceTime, 0, 0, 0, 0);

            CartesianVector<Cartesian_ND> doSomthing(int time)
            {
                CartesianVector<Cartesian_ND> result = new CartesianVector<Cartesian_ND>(0, 0, 0, 0);

                Random rand = new Random(DateTime.Now.GetHashCode() + time);

                result += (rand.Next(-10, 20) * i) + (rand.Next(-10, 20) * j) + (rand.Next(-10, 20) * k);

                return result;
            }

            CartesianVector<Cartesian_ND> movement;
            for (int time = 0; time < 200; time++)
            {
                movement = new CartesianVector<Cartesian_ND>(0, 0, 0, 1);

                movement += doSomthing(time);

                loc.Move(movement);
            }
            
            Print(loc.Ordinates[0].ToString() + ", " + loc.Ordinates[1].ToString() + ", " + loc.Ordinates[2].ToString());
        }

        [TestMethod]
        public void Field_Test()
        {
            var space = new Cartesian_3D(Units.m, Units.m, Units.m);

            var loc0 = new Cartesian_3D_Coordinate(space, 0, 0, 0);
            var loc = new Cartesian_3D_Coordinate(space, 10, 0, 0);

            LocatedCartesianVector<Cartesian_3D> fieldEquasion(ICoordinate<Cartesian_3D> coordinate) =>new LocatedCartesianVector<Cartesian_3D>(coordinate, (decimal)(0.01 * -Math.Pow((double)coordinate.Ordinates[0], 2)), (decimal)(0.01 * -Math.Pow((double)coordinate.Ordinates[1], 2)), (decimal)(0.01 * -Math.Pow((double)coordinate.Ordinates[2], 2)));

            var flow = new VectorField<Cartesian_3D, LocatedCartesianVector<Cartesian_3D>>(space, new Func<ICoordinate<Cartesian_3D>, LocatedCartesianVector<Cartesian_3D>>(fieldEquasion));
            
            int count = 0;
            Print(loc.Ordinates[0].ToString() + ", " + loc.Ordinates[1].ToString() + ", " + loc.Ordinates[2].ToString());
            while ((loc.Ordinates[0] != loc0.Ordinates[0] || loc.Ordinates[1] != loc0.Ordinates[1] || loc.Ordinates[2] != loc0.Ordinates[2]) && count < 200)
            {
                loc.Move(flow.AtLoc(loc));
                Print(loc.ToString() + flow.CalculateAtLoc(loc).ToString());

                count++;
            }



            ScalarField<Cartesian_2D> potential;
            VectorField<Cartesian_2D, LocatedCartesianVector<Cartesian_2D>> EField;

            decimal q1 = 1;
            decimal q2 = -1;

            decimal EFieldEquasion(ICoordinate<Cartesian_2D> coordinate)
            {
                return (1 / (4 * (decimal)Math.PI * (decimal)0.00000000000885418781762039)) * ((q1 * q2) / (decimal)(Math.Pow((double)coordinate.Ordinates[0], 2) + Math.Pow((double)coordinate.Ordinates[1], 2)));
            }

            decimal EFieldPotential(ICoordinate<Cartesian_2D> coordinate)
            {
                return (1 / (4 * (decimal)Math.PI * (decimal)0.00000000000885418781762039)) * (q1 / (decimal)Math.Sqrt(Math.Pow((double)coordinate.Ordinates[0], 2) + Math.Pow((double)coordinate.Ordinates[1], 2)));
            }

            potential = new ScalarField<Cartesian_2D>(new Cartesian_2D(Units.m, Units.m), EFieldPotential);
        }

        [TestMethod]
        public void Symbolic_Test()
        {
            Variable A = new Variable("A");

            Variable r = new Variable("r");
            
            A.SetValue(Constant.PI * (r ^ 2));

            Print(A.GetEquasion(20));

            r.Initialise(5);

            Print("r = 5: " + A.Value);

            r.Value = 10;

            Print("r = 10: " + A.Value);

            Print();


            Variable y = new Variable("y");

            Variable m = new Variable("m").Initialise(2);

            Variable x = new Variable("x");

            Variable c = new Variable("c").Initialise(1);

            Print(y.GetEquasion());

            y.SetValue(m * x + c);

            Print(y.GetEquasion());

            x.SetValue(new Variable("i", 1) + new Variable("j", 1) + new Variable("k", 1));

            Print(y.GetEquasion());

            Print(y.GetEquasion(20));// Not evaluating j and k

            Print("y = " + y.Value);

            Print();


            Variable theta = new Variable("theta").Initialise(Constant.PI);

            Variable result = Variable.tan(theta);

            Print(result.GetEquasion());
            Print(result.GetEquasion(20));
            Print(result.Value);

            Print();


            Print(Constant.PHI.symbol + " = " + Constant.PHI.Value);
        }

        [TestMethod]
        public void Deleteme_Test()
        {
            //QuasarCode.Library.Maths.Matrices.
        }
    }
}