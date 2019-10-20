using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// Root interface in the dice cup type hierarchy.
    /// </summary>
    public interface IDiceCup
    {
        /// <summary>
        /// Number of dice stored.
        /// </summary>
        int Count {  get; }

        /// <summary>
        /// Rolls all the dice. Returns each individual result.
        /// </summary>
        /// <param name="suppressEmptyExeption">Suppress the exeption raised when the cup is empty</param>
        /// <returns>Array of integers</returns>
        int[] Roll(bool suppressEmptyExeption = false);

        /// <summary>
        /// Rolls all the dice. Returns the sum of the results.
        /// </summary>
        /// <param name="suppressEmptyExeption">Suppress the exeption raised when the cup is empty</param>
        /// <returns>Integer</returns>
        int RollTotal(bool suppressEmptyExeption = false);
    }
}
