using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A collection of 52+ unique playing cards. The exact number can vary dependant on the number of jokers added
    /// </summary>
    public sealed class Deck : System.Collections.ObjectModel.Collection<PlayingCard>
    {
        /// <summary>
        /// The cards in the deck (including the jokers).
        /// </summary>
        public readonly PlayingCard[] Cards;

        /// <summary>
        /// The number of jokers in this deck
        /// </summary>
        public int Jokers { get; private set; }

        /// <summary>
        /// Creates a new Deck instance of 52 cards along with a specified number of jokers (deafult is 0)
        /// </summary>
        /// <param name="jokers">Number of jokers to add to the standard 52 cards</param>
        public Deck(int jokers = 0)
        {
            foreach (string suit in Enum.GetNames(typeof(PlayingCard.AllowedSuits)))
            {
                if (suit != Enum.GetName(typeof(PlayingCard.AllowedSuits), PlayingCard.AllowedSuits.J))
                {
                    foreach (string value in Enum.GetNames(typeof(PlayingCard.AllowedValues)))
                    {
                        if (value != Enum.GetName(typeof(PlayingCard.AllowedValues), PlayingCard.AllowedValues.Jo))
                        {
                            Add(new PlayingCard((PlayingCard.AllowedValues)Enum.Parse(typeof(PlayingCard.AllowedValues), value, false), (PlayingCard.AllowedSuits)Enum.Parse(typeof(PlayingCard.AllowedSuits), suit, false)));
                        }
                    }
                }
            }

            for (int i = 0; i < jokers; i++)
            {
                Add(new PlayingCard(PlayingCard.AllowedValues.Jo, PlayingCard.AllowedSuits.J));
            }

            Cards = Items.ToArray();
        }
        
        /// <summary>
        /// Deals the deck into a list of groups untill the deck is empty
        /// </summary>
        /// <param name="hands">The groups (ICardGroup's) to deal into</param>
        public void Deal(ref List<ICardGroup> hands)
        {
            Random randomiser = new Random();

            while (Items.Count > 0)
            {
                for (int i = 0; i < hands.Count; i++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands[i].Add((IPlayingCard)Items[card]);

                        Items.RemoveAt(card);
                    }
                    else
                    {
                        break;
                    }
                }
            }
        }

        /// <summary>
        /// Deals a set number of cards from the deck into a list of groups
        /// </summary>
        /// <param name="hands">The hands to deal into</param>
        /// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        /// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        public void Deal(ref List<ICardGroup> hands, int cardsPerHand, bool suppressEmptyException = false)
        {
            if (!suppressEmptyException && cardsPerHand * hands.Count > Items.Count)
            {
                throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
            }

            Random randomiser = new Random();

            for (int i = 0; i < cardsPerHand; i++)
            {
                for (int i2 = 0; i2 < hands.Count; i2++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands[i2].Add((IPlayingCard)Items[card]);

                        Items.RemoveAt(card);
                    }
                    else
                    {
                        break;
                    }
                }

                if (Items.Count == 0)
                {
                    break;
                }
            }
        }

        /// <summary>
        /// Deals a set number of cards from the deck into a list of groups and then dumps the rest into a group
        /// </summary>
        /// <param name="hands">The hands to deal into</param>
        /// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        /// <param name="group">The group to dump any remaining cards into</param>
        /// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        public void Deal(ref List<ICardGroup> hands, int cardsPerHand, ref ICardGroup group, bool suppressEmptyException = false)
        {
            if (!suppressEmptyException && cardsPerHand * hands.Count > Items.Count)
            {
                throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
            }

            Random randomiser = new Random();

            for (int i = 0; i < cardsPerHand; i++)
            {
                for (int i2 = 0; i2 < hands.Count; i2++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands[i2].Add((IPlayingCard)Items[card]);

                        Items.RemoveAt(card);
                    }
                    else
                    {
                        break;
                    }

                    if (Items.Count == 0)
                    {
                        break;
                    }
                }
            }

            while (Items.Count > 0)
            {
                int card = randomiser.Next(0, Items.Count);

                group.Add((IPlayingCard)Items[card]);

                Items.RemoveAt(card);
            }
        }

        /// <summary>
        /// Deals a set number of cards from the deck into a list of groups and then deals the remaining cards to a list of groups
        /// </summary>
        /// <param name="hands">The hands to deal into</param>
        /// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        /// <param name="groups">The groups to deal any remaining cards into</param>
        /// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        public void Deal(ref List<ICardGroup> hands, int cardsPerHand, ref List<ICardGroup> groups, bool suppressEmptyException = false)
        {
            if (!suppressEmptyException && cardsPerHand * hands.Count > Items.Count)
            {
                throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
            }

            Random randomiser = new Random();

            for (int i = 0; i < cardsPerHand; i++)
            {
                for (int i2 = 0; i2 < hands.Count; i2++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands[i2].Add((IPlayingCard)Items[card]);

                        Items.RemoveAt(card);
                    }
                    else
                    {
                        break;
                    }

                    if (Items.Count == 0)
                    {
                        break;
                    }
                }
            }

            while (Items.Count > 0)
            {
                for (int i = 0; i < groups.Count; i++)
                {
                    if (groups.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        groups[i].Add((IPlayingCard)Items[card]);

                        Items.RemoveAt(card);
                    }
                    else
                    {
                        break;
                    }
                }
            }
        }

        /// <summary>
        /// Reset the deck so that it has all the cards it started with
        /// </summary>
        public void Reset()
        {
            Items.Clear();

            foreach (PlayingCard card in Cards) { Items.Add(card); } 
        }
    }
}
