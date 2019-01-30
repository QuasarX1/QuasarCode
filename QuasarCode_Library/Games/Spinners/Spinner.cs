using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace QuasarCode.Library.Games.Spinners
{
    /// <summary>
    /// Creates spinner objects with n sides and labels. Labels are selected and returned by calling the avalable methods.
    /// </summary>
    /// <typeparam name="T">Data type of labels</typeparam>
    public class Spinner<T>: ISpinner<T>
    {
        /// <summary>
        /// Random number generator
        /// </summary>
        private Random Generator;

        /// <summary>
        /// Array of side labels
        /// </summary>
        public T[] Labels { get; }

        /// <summary>
        /// Number of sides/labels
        /// </summary>
        public int Sides { get; }

        /// <summary>
        /// Creates a new spinner object.
        /// </summary>
        /// <param name="labels">Array of labels - one for each side.</param>
        public Spinner(params T[] labels)
        {
            Labels = labels;

            Sides = Labels.Length;

            Generator = new Random();
        }

        /// <summary>
        /// Creates a new spinner object.
        /// </summary>
        /// <param name="labels">Array of labels - one for each side.</param>
        public Spinner(ICollection<T> labels)
        {
            Labels = labels.ToArray();

            Sides = Labels.Length;

            Generator = new Random();
        }

        /// <summary>
        /// Creates a new spinner object.
        /// </summary>
        /// <param name="labels">Array of labels - one for each side.</param>
        /// <param name="seed">Seed for the random generator.</param>
        public Spinner(ICollection<T> labels, int seed)
        {
            Labels = labels.ToArray();

            Sides = Labels.Length;

            Generator = new Random(seed);
        }

        /// <summary>
        /// Randomly selects a side and retuns the side and the corisponding label.
        /// </summary>
        /// <returns>Tuple with int and label type</returns>
        public Tuple<int, T> ContextSpin()
        {
            int index = Generator.Next(0, Sides);

            return new Tuple<int, T>(index, Labels[index]);
        }

        /// <summary>
        /// Randomly selects a side and retuns the corisponding label.
        /// </summary>
        /// <returns>Side label</returns>
        public T Spin()
        {
            return Labels[Generator.Next(0, Sides)];
        }

        /// <summary>
        /// Randomly selects a side and retuns the side number.
        /// </summary>
        /// <returns>Side number</returns>
        public int IndexSpin()
        {
            return Generator.Next(0, Sides);
        }
        
    }
}
