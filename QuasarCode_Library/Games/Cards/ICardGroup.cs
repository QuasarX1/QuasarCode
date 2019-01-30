using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A collection of IPlaying cards
    /// </summary>
    public interface ICardGroup<T> where T : IPlayingCard
    {
        /// <summary>
        /// Name of the collection
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Add a card to the collection
        /// </summary>
        /// <param name="card">The card to add</param>
        void Add(T card);

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        T Remove(int index);

        /// <summary>
        /// Randomises the order of the cards in the group
        /// </summary>
        void Shuffle();

        /// <summary>
        /// Event handler for requesting the return of cards
        /// </summary>
        /// <param name="sender">The object triggering the event</param>
        void ReturnCards(object sender);
    }
}
