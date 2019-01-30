using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Games.Cards
{
    /// <summary>
    /// A card from a standard deck of 52 playing cards
    /// </summary>
    public class PlayingCard : IPlayingCard
    {
        /// <summary>
        /// The card's value
        /// </summary>
        public AllowedValues Value { get; }

        /// <summary>
        /// The card's suit
        /// </summary>
        public AllowedSuits Suit { get; }
        
        /// <summary>
        /// Creates a new PlayingCard instance
        /// </summary>
        /// <param name="value">The card's value</param>
        /// <param name="suit">The card's suit</param>
        public PlayingCard(AllowedValues value, AllowedSuits suit)
        {
            Value = value;

            Suit = suit;
        }



        private static readonly string[] ValueStrings = new string[] { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" };

        /// <summary>
        /// Enum of card values from ace to king
        /// </summary>
        public enum AllowedValues
        {
            /// <summary>Ace</summary>
            A,

            /// <summary>Two</summary>
            Two,

            /// <summary>Three</summary>
            Three,

            /// <summary>Four</summary>
            Four,

            /// <summary>Five</summary>
            Five,

            /// <summary>Six</summary>
            Six,

            /// <summary>Seven</summary>
            Seven,

            /// <summary>Eight</summary>
            Eight,

            /// <summary>Nine</summary>
            Nine,

            /// <summary>Ten</summary>
            Ten,

            /// <summary>Jack</summary>
            J,

            /// <summary>Queen</summary>
            Q,

            /// <summary>King</summary>
            K,

            /// <summary>Joker</summary>
            Jo
        }

        /// <summary>
        /// Retrive the string counterpart to the AllowedValues enum value
        /// </summary>
        /// <param name="value">Card value from AllowedValues</param>
        /// <returns>String representing the provided value</returns>
        public static string GetValueString(AllowedValues value)
        {
            return ValueStrings[(int)value];
        }


        private static readonly string[] SuitStrings = new string[] { "Heart", "Club", "Dimond", "Spade", "Joker" };

        /// <summary>
        /// Enum of card suits - hearts, clubs, dimonds, spades, joker
        /// </summary>
        public enum AllowedSuits
        {
            /// <summary>Heart</summary>
            H,

            /// <summary>Club</summary>
            C,

            /// <summary>Dimond</summary>
            D,

            /// <summary>Spade</summary>
            S,

            /// <summary>Joker</summary>
            J
        }

        /// <summary>
        /// Retrive the string counterpart to the AllowedSuits enum suit
        /// </summary>
        /// <param name="suit">Card suit from AllowedSuits</param>
        /// <returns>String representing the provided suit</returns>
        public static string GetSuitString(AllowedSuits suit)
        {
            return SuitStrings[(int)suit];
        }
    }
}
