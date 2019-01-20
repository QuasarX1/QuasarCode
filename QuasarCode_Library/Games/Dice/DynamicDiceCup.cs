using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// A mutable collection of NDice objects that are rolled together.
    /// </summary>
    public sealed class DynamicDiceCup : IDynamicDiceCup
    {
        /// <summary>
        /// List of the NDice objects rolled by the cup.
        /// </summary>
        public List<IDice> AllDice { get; private set; }

        /// <summary>
        /// Number of dice stored.
        /// </summary>
        public int Count { get { return AllDice.Count; } }

        /// <summary>
        /// Creates a new dynamic dice cup with no starting dice.
        /// </summary>
        public DynamicDiceCup()
        {
            AllDice = new List<IDice>();
        }

        /// <summary>
        /// Creates a new dynamic dice cup.
        /// </summary>
        /// <param name="sides">The number of sides on each dice</param>
        /// <param name="noOfDice">Number of dice to create</param>
        public DynamicDiceCup(int sides, int noOfDice)
        {
            AllDice = new List<IDice>();

            foreach (NDice dice in NDice.MultipleDice(sides, noOfDice))
            {
                AllDice.Add(dice);
            }
        }

        /// <summary>
        /// Creates a new dynamic dice cup.
        /// </summary>
        /// <param name="sides">Side numbers representing each unique dice</param>
        public DynamicDiceCup(params int[] sides)
        {
            AllDice = new List<IDice>();

            foreach (NDice dice in NDice.MultipleDice(sides))
            {
                AllDice.Add(dice);
            }
        }

        /// <summary>
        /// Creates a new dynamic dice cup.
        /// </summary>
        /// <param name="sides">Collection of side numbers representing unique dice</param>
        public DynamicDiceCup(ICollection<int> sides)
        {
            AllDice = new List<IDice>();

            foreach (NDice dice in NDice.MultipleDice(sides))
            {
                AllDice.Add(dice);
            }
        }

        /// <summary>
        /// Rolls all the dice. Returns each individual result.
        /// </summary>
        /// <param name="suppressEmptyExeption">Suppress the exeption raised when the cup is empty</param>
        /// <exception cref="InvalidOperationException" />
        /// <returns>Array of integers</returns>
        public int[] Roll(bool suppressEmptyExeption = false)
        {
            if (!suppressEmptyExeption && Count == 0)
            {
                throw new InvalidOperationException("There are no dice in the cup.");
            }


            List<int> results = new List<int>();

            foreach (IDice dice in AllDice)
            {
                results.Add(dice.Roll());
            }

            return results.ToArray();
        }

        /// <summary>
        /// Rolls all the dice. Returns the sum of the results.
        /// </summary>
        /// <param name="suppressEmptyExeption">Suppress the exeption raised when the cup is empty</param>
        /// <exception cref="InvalidOperationException" />
        /// <returns>Integer</returns>
        public int RollTotal(bool suppressEmptyExeption = false)
        {
            if (!suppressEmptyExeption && Count == 0)
            {
                throw new InvalidOperationException("There are no dice in the cup.");
            }


            int result = 0;

            foreach (IDice dice in AllDice)
            {
                result += dice.Roll();
            }

            return result;
        }

        /// <summary />
        /// <param name="index">Location in the collection</param>
        /// <returns>NDice</returns>
        public IDice this[int index]
        {
            get
            {
                try
                {
                    return AllDice[index];
                }
                catch (Exception)
                {
                    throw;
                }
            }

            set
            {
                try
                {
                    AllDice[index] = value;
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }

        /// <summary>
        /// Adds a dice to the cup
        /// </summary>
        /// <param name="dice">Dice to be added to the cup</param>
        public void PushDice(IDice dice)
        {
            AllDice.Add(dice);
        }

        /// <summary>
        /// Removes the last avalable dice in the cup
        /// </summary>
        /// <exception cref="InvalidOperationException" />
        /// <returns>NDice removed from cup</returns>
        public IDice PopDice()
        {
            if (Count == 0)
            {
                throw new InvalidOperationException("There are no dice in the cup.");
            }

            IDice oldDice = AllDice[Count - 1];

            AllDice.RemoveAt(Count - 1);

            return oldDice;
        }


        /// <summary>
        /// Adds a dice to a DynamicDiceCup instance
        /// </summary>
        /// <param name="cup">Dice cup to add the dice to</param>
        /// <param name="dice">Dice to be added to the cup</param>
        /// <returns>DynamicDiceCup with additional dice</returns>
        public static DynamicDiceCup operator+(DynamicDiceCup cup, IDice dice)
        {
            cup.PushDice(dice);

            return cup;
        }

        /// <summary>
        /// Removes the last avalable dice in a DynamicDiceCup instance
        /// </summary>
        /// <param name="cup">Dice cup to remove the dice from</param>
        /// <exception cref="InvalidOperationException" />
        /// <returns>DynamicDiceCup with last dice removed</returns>
        public static DynamicDiceCup operator --(DynamicDiceCup cup)
        {
            cup.PopDice();

            return cup;
        }
    }
}
