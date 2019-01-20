using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A stack data structure containing IPlayingCards
    /// </summary>
    public class CardStack : Stack<IPlayingCard>, ICardStack
    {
        /// <summary>
        /// Name of the collection
        /// </summary>
        public string Name { get; protected set; }

        /// <summary>
        /// Add a card to the collection
        /// </summary>
        /// <param name="card">The card to add</param>
        public void Add(IPlayingCard card)
        {
            Push(card);
        }

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        public IPlayingCard Remove(int index)
        {
            int popCount = this.Count - 1 - index;

            Stack<IPlayingCard> holding = new Stack<IPlayingCard>();
            for (int i = 0; i < popCount; i++)
            {
                holding.Push(this.Pop());
            }

            IPlayingCard element = this.Pop();

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

            List<IPlayingCard> newOrder = new List<IPlayingCard>();

            List<IPlayingCard> currentOrder = new List<IPlayingCard>();

            while (this.Count > 0)
            {
                currentOrder.Add(this.Pop());
            }

            while (currentOrder.Count > 0)
            {
                int position = generator.Next();

                newOrder.Add(currentOrder[position]);

                currentOrder.RemoveAt(position);
            }

            foreach (IPlayingCard card in newOrder)
            {
                this.Push(card);
            }
        }
    }
}
