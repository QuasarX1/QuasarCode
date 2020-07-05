using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

using QuasarCode.Library.Tools;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// An immutable collection of NDice objects that are rolled together.
    /// </summary>
    public sealed class DiceCup : IStaticDiceCup
    {
        /// <summary>
        /// Array of the NDice objects rolled by the cup.
        /// </summary>
        public IDice[] AllDice { get; private set; }

        /// <summary>
        /// Number of dice stored.
        /// </summary>
        public int Count { get { return AllDice.Length; } }

        /// <summary>
        /// Creates a new dice cup.
        /// </summary>
        /// <param name="sides">The number of sides on each dice</param>
        /// <param name="noOfDice">Number of dice to create</param>
        public DiceCup(int sides, int noOfDice)
        {
            List<NDice> allDice = new List<NDice>();
            
            foreach (NDice dice in NDice.MultipleDice(sides, noOfDice))
            {
                allDice.Add(dice);
            }

            AllDice = allDice.ToArray();
        }

        /// <summary>
        /// Creates a new dice cup.
        /// </summary>
        /// <param name="sides">Side numbers representing each unique dice</param>
        public DiceCup(params int[] sides)
        {
            List<NDice> allDice = new List<NDice>();

            foreach (NDice dice in NDice.MultipleDice(sides))
            {
                allDice.Add(dice);
            }

            AllDice = allDice.ToArray();
        }

        /// <summary>
        /// Creates a new dice cup.
        /// </summary>
        /// <param name="sides">Collection of side numbers representing unique dice</param>
        public DiceCup(ICollection<int> sides)
        {
            List<NDice> allDice = new List<NDice>();

            foreach (NDice dice in NDice.MultipleDice(sides))
            {
                allDice.Add(dice);
            }

            AllDice = allDice.ToArray();
        }

        /// <summary>
        /// Rolls all the dice. Returns each individual result.
        /// </summary>
        /// <param name="suppressEmptyExeption">Suppress the exeption raised when the cup is empty</param>
        /// <returns>Array of integers</returns>
        public int[] Roll(bool suppressEmptyExeption = false)
        {
            if (!suppressEmptyExeption && Count == 0)
            {
                throw new InvalidOperationException("There are no dice in the cup.");
            }

            List<int> results = new List<int>();

            foreach (NDice dice in AllDice)
            {
                results.Add(dice.Roll());
            }

            return results.ToArray();
        }

        /// <summary>
        /// Rolls all the dice. Returns the sum of the results.
        /// </summary>
        /// <param name="suppressEmptyExeption">Suppress the exeption raised when the cup is empty</param>
        /// <returns>Integer</returns>
        public int RollTotal(bool suppressEmptyExeption = false)
        {
            if (!suppressEmptyExeption && Count == 0)
            {
                throw new InvalidOperationException("There are no dice in the cup.");
            }

            int result = 0;

            foreach (NDice dice in AllDice)
            {
                result += dice.Roll();
            }

            return result;
        }
    }
}
