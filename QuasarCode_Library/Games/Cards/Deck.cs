using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A collection of 52+ unique playing cards. The exact number can vary dependant on the number of jokers added
    /// </summary>
    public sealed class Deck : CardGroup<PlayingCard>
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
        /// <param name="name">The name of the deck</param>
        /// <param name="jokers">Number of jokers to add to the standard 52 cards</param>
        public Deck(string name, int jokers = 0) : base(name)
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
        /// Initialises a card group for use with the deck
        /// </summary>
        /// <param name="groups">The group(s) to be initialised</param>
        public void InitialiseGroup(params ICardGroup<PlayingCard>[] groups)
        {
            foreach (ICardGroup<PlayingCard> group in groups)
            {
                if (!subscribers.Contains(group))
                {
                    subscribers.Add(group);

                    ReturnCards += group.ReturnCards;
                }
            }
        }

        /// <summary>
        /// Removes card groups from use with the deck
        /// </summary>
        /// <param name="groups">The group(s) to remove</param>
        public void ReleaseGroup(params ICardGroup<PlayingCard>[] groups)
        {
            foreach (ICardGroup<PlayingCard> group in groups)
            {
                if (subscribers.Contains(group))
                {
                    subscribers.Remove(group);

                    ReturnCards -= group.ReturnCards;
                }
            }
        }
        

        /// <summary>
        /// Deals the deck into a list of groups untill the deck is empty
        /// </summary>
        /// <param name="hands">The groups (ICardGroup's) to deal into</param>
        public void Deal<T>(ICollection<T> hands) where T : ICardGroup<PlayingCard>
        {
            foreach (ICardGroup<PlayingCard> hand in hands)
            {
                if (!subscribers.Contains(hand))
                {
                    throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
                }
            }

            Random randomiser = new Random();

            while (Items.Count > 0)
            {
                for (int i = 0; i < hands.Count; i++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands.ElementAt(i).Add(Items[card]);
                        //hands[i].Add(Items[card]);

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
        /// Deals the deck into a list of groups untill the deck is empty
        /// </summary>
        /// <param name="hands">The groups (ICardGroup's) to deal into</param>
        public void Deal<T>(params T[] hands) where T : ICardGroup<PlayingCard>
        {
            foreach (ICardGroup<PlayingCard> hand in hands)
            {
                if (!subscribers.Contains(hand))
                {
                    throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
                }
            }

            Random randomiser = new Random();

            while (Items.Count > 0)
            {
                for (int i = 0; i < hands.Length; i++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands[i].Add(Items[card]);

                        Items.RemoveAt(card);
                    }
                    else
                    {
                        break;
                    }
                }
            }
        }


        ///// <summary>
        ///// Deals a set number of cards from the deck into a list of groups
        ///// </summary>
        ///// <param name="hands">The hands to deal into</param>
        ///// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        ///// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        //public void DealDeal<T>(T[] hands, int cardsPerHand, bool suppressEmptyException = false) where T : ICardGroup<PlayingCard>
        //{
        //    if (!suppressEmptyException && cardsPerHand * hands.Count() > Items.Count)
        //    {
        //        throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
        //    }

        //    foreach (ICardGroup<PlayingCard> hand in hands)
        //    {
        //        if (!subscribers.Contains(hand))
        //        {
        //            subscribers.Add(hand);

        //            ReturnCards += hand.ReturnCards;
        //        }
        //    }

        //    Random randomiser = new Random();

        //    for (int i = 0; i < cardsPerHand; i++)
        //    {
        //        for (int i2 = 0; i2 < hands.Count(); i2++)
        //        {
        //            if (Items.Count > 0)
        //            {
        //                int card = randomiser.Next(0, Items.Count);

        //                hands[i2].Add(Items[card]);

        //                Items.RemoveAt(card);
        //            }
        //            else
        //            {
        //                break;
        //            }
        //        }

        //        if (Items.Count == 0)
        //        {
        //            break;
        //        }
        //    }
        //}

        /// <summary>
        /// Deals a set number of cards from the deck into a list of groups
        /// </summary>
        /// <param name="hands">The hands to deal into</param>
        /// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        /// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        public void Deal<T>(ICollection<T> hands, int cardsPerHand, bool suppressEmptyException = false) where T : ICardGroup<PlayingCard>
        {
            if (!suppressEmptyException && cardsPerHand * hands.Count > Items.Count)
            {
                throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
            }

            foreach (ICardGroup<PlayingCard> hand in hands)
            {
                if (!subscribers.Contains(hand))
                {
                    throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
                }
            }

            Random randomiser = new Random();

            for (int i = 0; i < cardsPerHand; i++)
            {
                for (int i2 = 0; i2 < hands.Count; i2++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands.ElementAt(i2).Add(Items[card]);
                        //hands[i2].Add(Items[card]);

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


        ///// <summary>
        ///// Deals a set number of cards from the deck into a list of groups and then dumps the rest into a group
        ///// </summary>
        ///// <param name="hands">The hands to deal into</param>
        ///// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        ///// <param name="group">The group to dump any remaining cards into</param>
        ///// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        //public void Deal<T>(T[] hands, int cardsPerHand, T group, bool suppressEmptyException = false) where T : ICardGroup<PlayingCard>
        //{
        //    if (!suppressEmptyException && cardsPerHand * hands.Count() > Items.Count)
        //    {
        //        throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
        //    }

        //    foreach (ICardGroup<PlayingCard> hand in hands)
        //    {
        //        if (!subscribers.Contains(hand))
        //        {
        //            subscribers.Add(hand);

        //            ReturnCards += hand.ReturnCards;
        //        }
        //    }

        //    if (!subscribers.Contains(group))
        //    {
        //        subscribers.Add(group);

        //        ReturnCards += group.ReturnCards;
        //    }

        //    Random randomiser = new Random();

        //    for (int i = 0; i < cardsPerHand; i++)
        //    {
        //        for (int i2 = 0; i2 < hands.Count(); i2++)
        //        {
        //            if (Items.Count > 0)
        //            {
        //                int card = randomiser.Next(0, Items.Count);

        //                hands[i2].Add(Items[card]);

        //                Items.RemoveAt(card);
        //            }
        //            else
        //            {
        //                break;
        //            }

        //            if (Items.Count == 0)
        //            {
        //                break;
        //            }
        //        }
        //    }

        //    while (Items.Count > 0)
        //    {
        //        int card = randomiser.Next(0, Items.Count);

        //        group.Add(Items[card]);

        //        Items.RemoveAt(card);
        //    }
        //}

        /// <summary>
        /// Deals a set number of cards from the deck into a list of groups and then dumps the rest into a group
        /// </summary>
        /// <param name="hands">The hands to deal into</param>
        /// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        /// <param name="group">The group to dump any remaining cards into</param>
        /// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        public void Deal<T>(ICollection<T> hands, int cardsPerHand, T group, bool suppressEmptyException = false) where T : ICardGroup<PlayingCard>
        {
            if (!suppressEmptyException && cardsPerHand * hands.Count > Items.Count)
            {
                throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
            }

            foreach (ICardGroup<PlayingCard> hand in hands)
            {
                if (!subscribers.Contains(hand))
                {
                    throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
                }
            }

            if (!subscribers.Contains(group))
            {
                throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
            }

            Random randomiser = new Random();

            for (int i = 0; i < cardsPerHand; i++)
            {
                for (int i2 = 0; i2 < hands.Count; i2++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands.ElementAt(i2).Add(Items[card]);
                        //hands[i2].Add(Items[card]);

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

                group.Add(Items[card]);

                Items.RemoveAt(card);
            }
        }


        ///// <summary>
        ///// Deals a set number of cards from the deck into a list of groups and then deals the remaining cards to a list of groups
        ///// </summary>
        ///// <param name="hands">The hands to deal into</param>
        ///// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        ///// <param name="groups">The groups to deal any remaining cards into</param>
        ///// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        //public void Deal<T>(T[] hands, int cardsPerHand, T[] groups, bool suppressEmptyException = false) where T : ICardGroup<PlayingCard>
        //{
        //    if (!suppressEmptyException && cardsPerHand * hands.Count() > Items.Count)
        //    {
        //        throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
        //    }

        //    foreach (ICardGroup<PlayingCard> hand in hands)
        //    {
        //        if (!subscribers.Contains(hand))
        //        {
        //            subscribers.Add(hand);

        //            ReturnCards += hand.ReturnCards;
        //        }
        //    }

        //    foreach (ICardGroup<PlayingCard> group in groups)
        //    {
        //        if (!subscribers.Contains(group))
        //        {
        //            subscribers.Add(group);

        //            ReturnCards += group.ReturnCards;
        //        }
        //    }

        //    Random randomiser = new Random();

        //    for (int i = 0; i < cardsPerHand; i++)
        //    {
        //        for (int i2 = 0; i2 < hands.Count(); i2++)
        //        {
        //            if (Items.Count > 0)
        //            {
        //                int card = randomiser.Next(0, Items.Count);

        //                hands[i2].Add(Items[card]);

        //                Items.RemoveAt(card);
        //            }
        //            else
        //            {
        //                break;
        //            }

        //            if (Items.Count == 0)
        //            {
        //                break;
        //            }
        //        }
        //    }

        //    while (Items.Count > 0)
        //    {
        //        for (int i = 0; i < groups.Count(); i++)
        //        {
        //            if (groups.Count() > 0)
        //            {
        //                int card = randomiser.Next(0, Items.Count);

        //                groups[i].Add(Items[card]);

        //                Items.RemoveAt(card);
        //            }
        //            else
        //            {
        //                break;
        //            }
        //        }
        //    }
        //}

        /// <summary>
        /// Deals a set number of cards from the deck into a list of groups and then deals the remaining cards to a list of groups
        /// </summary>
        /// <param name="hands">The hands to deal into</param>
        /// <param name="cardsPerHand">The number of cards to deal to each hand</param>
        /// <param name="groups">The groups to deal any remaining cards into</param>
        /// <param name="suppressEmptyException">Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand</param>
        public void Deal<T>(ICollection<T> hands, int cardsPerHand, ICollection<T> groups, bool suppressEmptyException = false) where T : ICardGroup<PlayingCard>
        {
            if (!suppressEmptyException && cardsPerHand * hands.Count > Items.Count)
            {
                throw new InvalidOperationException("There aren't enough cards in the deck to do this.");
            }

            foreach (ICardGroup<PlayingCard> hand in hands)
            {
                if (!subscribers.Contains(hand))
                {
                    throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
                }
            }

            foreach (ICardGroup<PlayingCard> group in groups)
            {
                if (!subscribers.Contains(group))
                {
                    throw new ArgumentException("One of the card groups provided wasn't initialised for use with this deck.");
                }
            }

            Random randomiser = new Random();

            for (int i = 0; i < cardsPerHand; i++)
            {
                for (int i2 = 0; i2 < hands.Count; i2++)
                {
                    if (Items.Count > 0)
                    {
                        int card = randomiser.Next(0, Items.Count);

                        hands.ElementAt(i2).Add(Items[card]);
                        //hands[i2].Add(Items[card]);

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

                        groups.ElementAt(i).Add(Items[card]);
                        //groups[i].Add(Items[card]);

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
        /// Reset the deck so that it has all the cards it started with and asks all ICardGroups dealt to to remove references to the cards
        /// </summary>
        public void Reset()
        {
            Items.Clear();

            ReturnCards?.Invoke(this);

            foreach (PlayingCard card in Cards) { Items.Add(card); } 
        }



        private List<ICardGroup<PlayingCard>> subscribers = new List<ICardGroup<PlayingCard>>();

        /// <summary>
        /// Request that all subscribers remove their held card objects
        /// </summary>
        new public event Action<object> ReturnCards;
    }
}
