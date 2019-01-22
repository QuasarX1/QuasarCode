using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A stack data structure containing IPlayingCards
    /// </summary>
    public class CardStack<T> : Stack<T>, ICardStack<T> where T : IPlayingCard
    {
        /// <summary>
        /// Name of the collection
        /// </summary>
        public string Name { get; protected set; }

        /// <summary>
        /// Creates an new CardStack instance
        /// </summary>
        /// <param name="name">The name of the stack</param>
        public CardStack(string name)
        {
            Name = name;
        }

        /// <summary>
        /// Add a card to the collection
        /// </summary>
        /// <param name="card">The card to add</param>
        public void Add(T card)
        {
            Push(card);
        }

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        public T Remove(int index)
        {
            int popCount = this.Count - 1 - index;

            Stack<T> holding = new Stack<T>();
            for (int i = 0; i < popCount; i++)
            {
                holding.Push(this.Pop());
            }

            T element = this.Pop();

            for (int i = 0; i < popCount; i++)
            {
                this.Push(holding.Pop());
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
                currentOrder.Add(this.Pop());
            }

            while (currentOrder.Count > 0)
            {
                int position = generator.Next(currentOrder.Count);

                newOrder.Add(currentOrder[position]);

                currentOrder.RemoveAt(position);
            }

            foreach (T card in newOrder)
            {
                this.Push(card);
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
