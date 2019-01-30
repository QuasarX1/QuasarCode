using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A collection of IPlaying cards
    /// </summary>
    public class CardGroup<T> : System.Collections.ObjectModel.Collection<T>, ICardGroup<T> where T : IPlayingCard
    {
        /// <summary>
        /// Name of the collection
        /// </summary>
        public string Name { get; protected set; }

        /// <summary>
        /// Creates a CardGroup instance with no cards
        /// </summary>
        /// <param name="name">The name of the group</param>
        public CardGroup(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Creates a CardGroup instance with a starting set of cards
        /// </summary>
        /// <param name="name">The name of the group</param>
        /// <param name="cards">The cards to be added to the group</param>
        public CardGroup(string name, params IPlayingCard[] cards)
        {
            Name = name;

            foreach (IPlayingCard card in cards)
            {
                Items.Add((T)card);
            }
        }

        /// <summary>
        /// Creates a CardGroup instance with a starting set of cards
        /// </summary>
        /// <param name="name">The name of the group</param>
        /// <param name="cards">The cards to be added to the group</param>
        public CardGroup(string name, IEnumerable<IPlayingCard> cards)
        {
            Name = name;

            foreach (IPlayingCard card in cards)
            {
                Items.Add((T)card);
            }
        }

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        public T Remove(int index)
        {
            T element = Items[index];

            Items.RemoveAt(index);

            return element;
        }

        /// <summary>
        /// Randomises the order of the cards in the group
        /// </summary>
        public void Shuffle()
        {
            Random generator = new Random();

            List<IPlayingCard> newOrder = new List<IPlayingCard>();

            List<IPlayingCard> currentOrder = new List<IPlayingCard>();

            while (this.Count > 0)
            {
                currentOrder.Add(this.Remove(0));
            }

            while (currentOrder.Count > 0)
            {
                int position = generator.Next(currentOrder.Count);

                newOrder.Add(currentOrder[position]);

                currentOrder.RemoveAt(position);
            }

            foreach (IPlayingCard card in newOrder)
            {
                this.Add((T)card);
            }
        }

        /// <summary>
        /// Event handler for requesting the return of cards
        /// </summary>
        /// <param name="sender">The object triggering the event</param>
        public void ReturnCards(object sender)
        {
            Items.Clear();
        }
    }
}
