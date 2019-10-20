using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// A dice that can be rolled to produce an integer result starting from 1
    /// </summary>
    public interface IDice
    {
        /// <summary>
        /// Number of sides on the dice
        /// </summary>
        int Sides { get; }

        /// <summary>
        /// Rolls the dice
        /// </summary>
        /// <returns>Integer outcome of the roll</returns>
        int Roll();
    }
}
