using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// A dice with a specified number of sides
    /// </summary>
    public class NDice : IDice
    {
        private Random Generator;

        /// <summary>
        /// Number of sides on the dice
        /// </summary>
        public int Sides { get; }

        /// <summary>
        /// Creates a new NDice instance
        /// </summary>
        /// <param name="sides">Number of sides on the dice</param>
        public NDice(int sides)
        {
            Sides = sides;

            Generator = new Random();
        }

        /// <summary>
        /// Creates a new NDice instance
        /// </summary>
        /// <param name="sides">Number of sides on the dice</param>
        /// <param name="seed">Seed for the random generator</param>
        public NDice(int sides, int seed)
        {
            Sides = sides;

            Generator = new Random(seed);
        }

        /// <summary>
        /// Rolls the dice
        /// </summary>
        /// <returns>Integer outcome of the roll</returns>
        public int Roll()
        {
            return Generator.Next(1, Sides + 1);
        }


        /// <summary>
        /// Convenience method for creating multiple dice
        /// </summary>
        /// <param name="sides">The number of sides on each dice</param>
        /// <param name="noOfDice">Number of dice to create</param>
        /// <returns>Yeilds dice to produce an IEnumerable</returns>
        public static System.Collections.IEnumerable MultipleDice(int sides, int noOfDice)
        {
            Random randomiser = new Random();

            for (int i = 0; i < noOfDice; i++)
            {
                yield return new NDice(sides, randomiser.Next(100000, 999999));
            }
        }

        /// <summary>
        /// Convenience method for creating multiple dice
        /// </summary>
        /// <param name="sides">Side numbers representing each unique dice</param>
        /// <returns>Yeilds dice to produce an IEnumerable</returns>
        public static System.Collections.IEnumerable MultipleDice(params int[] sides)
        {
            Random randomiser = new Random();

            foreach (int size in sides)
            {
                yield return new NDice(size, randomiser.Next(100000, 999999));
            }
        }

        /// <summary>
        /// Convenience method for creating multiple dice
        /// </summary>
        /// <param name="sides">Collection of side numbers representing unique dice</param>
        /// <returns>Yeilds dice to produce an IEnumerable</returns>
        public static System.Collections.IEnumerable MultipleDice(ICollection<int> sides)
        {
            Random randomiser = new Random();

            foreach (int size in sides)
            {
                yield return new NDice(size, randomiser.Next(100000, 999999));
            }
        }
    }
}