using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A card from a standard deck of 52 playing cards
    /// </summary>
    public interface IPlayingCard
    {
        /// <summary>
        /// The card's value
        /// </summary>
        PlayingCard.AllowedValues Value { get; }

        /// <summary>
        /// The card's suit
        /// </summary>
        PlayingCard.AllowedSuits Suit { get; }
    }
}
