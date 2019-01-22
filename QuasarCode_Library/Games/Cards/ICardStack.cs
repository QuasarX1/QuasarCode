using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A stack data structure containing IPlayingCards
    /// </summary>
    public interface ICardStack<T> : ICardGroup<T> where T : IPlayingCard
    {
        /// <summary>
        /// Add a new card to the top of the stack
        /// </summary>
        /// <param name="card">The card to add</param>
        void Push(T card);

        /// <summary>
        /// Remove the card on top of the stack
        /// </summary>
        /// <returns>An IPlaying card</returns>
        T Pop();
    }
}
