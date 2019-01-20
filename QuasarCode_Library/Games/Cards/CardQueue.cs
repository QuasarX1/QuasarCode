using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Cards
{
    public class CardQueue : Queue<IPlayingCard>, ICardQueue
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
            Enqueue(card);
        }

        /// <summary>
        /// Remove a card from the collection at the specified index
        /// </summary>
        /// <param name="index">The index of the card to be removed</param>
        /// <returns>An IPlaying card</returns>
        public IPlayingCard Remove(int index)
        {
            Queue<IPlayingCard> holding = new Queue<IPlayingCard>();
            for (int i = 0; i < index; i++)
            {
                holding.Enqueue(this.Dequeue());
            }

            IPlayingCard element = this.Dequeue();

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

            List<IPlayingCard> newOrder = new List<IPlayingCard>();

            List<IPlayingCard> currentOrder = new List<IPlayingCard>();

            while (this.Count > 0)
            {
                currentOrder.Add(this.Dequeue());
            }

            while (currentOrder.Count > 0)
            {
                int position = generator.Next();

                newOrder.Add(currentOrder[position]);

                currentOrder.RemoveAt(position);
            }

            foreach (IPlayingCard card in newOrder)
            {
                this.Enqueue(card);
            }
        }
    }
}
