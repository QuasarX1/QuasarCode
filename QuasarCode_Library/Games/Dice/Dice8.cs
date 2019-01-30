using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Dice
{
    /// <summary>
    /// Simple didce with 8 sides.
    /// </summary>
    public sealed class Dice8 : NDice
    {
        /// <summary>
        /// Creates a new Dice8 instance
        /// </summary>
        public Dice8() : base(8) { }

        /// <summary>
        /// Creates a new Dice8 instance with a seed for the random generator
        /// </summary>
        /// <param name="seed">Seed for the random generator</param>
        public Dice8(int seed) : base(8, seed) { }
    }
}
