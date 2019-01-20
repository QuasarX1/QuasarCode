using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// Interface for dice cups where the number of dice can be changed.
    /// </summary>
    public interface IDynamicDiceCup : IDiceCup
    {
        /// <summary>
        /// List of the NDice objects rolled by the cup.
        /// </summary>
        List<NDice> AllDice { get; }

        /// <summary>
        /// Provides index access to the NDice list
        /// </summary>
        /// <param name="index">Location in the collection</param>
        /// <returns>NDice</returns>
        NDice this[int index] { get; set; }

        /// <summary>
        /// Adds a dice to the cup
        /// </summary>
        /// <param name="dice">Dice to be added to the cup</param>
        void PushDice(NDice dice);

        /// <summary>
        /// Removes the last avalable dice in the cup
        /// </summary>
        /// <exception cref="InvalidOperationException" />
        /// <returns>NDice removed from cup</returns>
        NDice PopDice();
    }
}
