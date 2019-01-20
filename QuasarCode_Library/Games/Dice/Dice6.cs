using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// Simple didce with 6 sides.
    /// </summary>
    public sealed class Dice6 : NDice
    {
        /// <summary>
        /// Creates a new Dice6 instance
        /// </summary>
        public Dice6() : base(6) { }

        /// <summary>
        /// Creates a new Dice6 instance with a seed for the random generator
        /// </summary>
        /// <param name="seed">Seed for the random generator</param>
        public Dice6(int seed) : base(6, seed) { }
    }
}
