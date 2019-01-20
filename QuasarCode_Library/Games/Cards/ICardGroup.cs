using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A collection of IPlaying cards
    /// </summary>
    public interface ICardGroup
    {
        /// <summary>
        /// Name of the collection
        /// </summary>
        string Name { get; }

        /// <summary>
        /// Add a card to the collection
        /// </summary>
        /// <param name="card">The card to add</param>
        void Add(IPlayingCard card);

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        IPlayingCard Remove(int index);

        /// <summary>
        /// Randomises the order of the cards in the group
        /// </summary>
        void Shuffle();
    }
}
