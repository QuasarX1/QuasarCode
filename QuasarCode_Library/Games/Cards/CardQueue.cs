using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A queue data structure containing IPlayingCards
    /// </summary>
    public class CardQueue<T> : Queue<T>, ICardQueue<T> where T : IPlayingCard
    {
        /// <summary>
        /// Name of the collection
        /// </summary>
        public string Name { get; protected set; }

        /// <summary>
        /// Creates an new CardQueue instance
        /// </summary>
        /// <param name="name">The name of the queue</param>
        public CardQueue(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Add a card to the collection
        /// </summary>
        /// <param name="card">The card to add</param>
        public void Add(T card)
        {
            Enqueue(card);
        }

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        public T Remove(int index)
        {
            Queue<T> holding = new Queue<T>();
            for (int i = 0; i < index; i++)
            {
                holding.Enqueue(this.Dequeue());
            }

            T element = this.Dequeue();

            for (int i = 0; i < index; i++)
            {
                this.Enqueue(holding.Dequeue());
            }

            return element;
        }

        /// <summary>
        /// Randomises the order of the cards in the group
        /// </summary>
        public void Shuffle()
        {
            Random generator = new Random();

            List<T> newOrder = new List<T>();

            List<T> currentOrder = new List<T>();

            while (this.Count > 0)
            {
                currentOrder.Add(this.Dequeue());
            }

            while (currentOrder.Count > 0)
            {
                int position = generator.Next(currentOrder.Count);

                newOrder.Add(currentOrder[position]);

                currentOrder.RemoveAt(position);
            }

            foreach (T card in newOrder)
            {
                this.Enqueue(card);
            }
        }

        /// <summary>
        /// Event handler for requesting the return of cards
        /// </summary>
        /// <param name="sender">The object triggering the event</param>
        public void ReturnCards(object sender)
        {
            this.Clear();
        }
    }
}
