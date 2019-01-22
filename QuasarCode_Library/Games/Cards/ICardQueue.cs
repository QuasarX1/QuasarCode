using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A queue data structure containing IPlayingCards
    /// </summary>
    public interface ICardQueue<T> : ICardGroup<T> where T : IPlayingCard
    {
        /// <summary>
        /// Add a new card to the end of the queue
        /// </summary>
        /// <param name="card">The card to add</param>
        void Enqueue(T card);

        /// <summary>
        /// Remove the card from the front of the queue
        /// </summary>
        /// <returns>An IPlaying card</returns>
        T Dequeue();
    }
}
