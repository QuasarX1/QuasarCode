using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Games.Spinners
{
    /// <summary>
    /// Interface for all Spinner objects.
    /// </summary>
    /// <typeparam name="T">Type of result data held by the spinner.</typeparam>
    public interface ISpinner<T>
    {
        /// <summary>
        /// Array of side labels
        /// </summary>
        T[] Labels { get; }

        /// <summary>
        /// Number of sides/labels
        /// </summary>
        int Sides { get; }

        /// <summary>
        /// Randomly selects a side and retuns the side and the corisponding label.
        /// </summary>
        /// <returns>Tuple with int and label type</returns>
        Tuple<int, T> ContextSpin();

        /// <summary>
        /// Randomly selects a side and retuns the corisponding label.
        /// </summary>
        /// <returns>Side label</returns>
        T Spin();

        /// <summary>
        /// Randomly selects a side and retuns the side number.
        /// </summary>
        /// <returns>Side number</returns>
        int IndexSpin();
    }
}
