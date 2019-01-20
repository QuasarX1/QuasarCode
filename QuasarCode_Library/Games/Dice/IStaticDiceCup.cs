using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// Interface for dice cups where the number of dice is fixed.
    /// </summary>
    public interface IStaticDiceCup : IDiceCup
    {
        /// <summary>
        /// Array of the NDice objects rolled by the cup.
        /// </summary>
        NDice[] AllDice { get; }
    }
}
