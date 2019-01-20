using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// Simple didce with 12 sides.
    /// </summary>
    public sealed class Dice12 : NDice
    {
        /// <summary>
        /// Creates a new Dice12 instance
        /// </summary>
        public Dice12() : base(12) { }

        /// <summary>
        /// Creates a new Dice12 instance with a seed for the random generator
        /// </summary>
        /// <param name="seed">Seed for the random generator</param>
        public Dice12(int seed) : base(12, seed) { }
    }
}
