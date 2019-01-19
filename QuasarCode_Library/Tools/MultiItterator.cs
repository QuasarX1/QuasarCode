using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.Linq;

namespace QuasarCode.Library.Tools
{
    /// <summary>
    /// Allows for itteration of multiple collections similtaniously.
    /// </summary>
    public class MultiItterator: IEnumerable<Tuple<int, object[]>>, IEnumerator<Tuple<int, object[]>>
    {
        /// <summary>
        /// The collections being itterated over.
        /// </summary>
        public readonly ICollection<object>[] Items;

        /// <summary>
        /// The number of items in the contained collections.
        /// </summary>
        public int Count { get; protected set; }

        /// <summary>
        /// Creates a new instance of the MultiItterator class. Collections must have the same length.
        /// </summary>
        /// <param name="items">IColections of objects.</param>
        public MultiItterator(params ICollection<object>[] items)
        {
            bool sameLength = true;
            for (int i = 1; i < items.Length; i++)
            {
                if (items[i].Count != items[0].Count)
                {
                    sameLength = false;
                    break;
                }
            }

            if (sameLength)
            {
                Items = items;
                Count = Items[0].Count;
            }
            else
            {
                throw new ArgumentException("The colections provided were not all of the same length.");
            }
        }


        /// <summary>
        /// Returns the index and data at the specified index in the collections.
        /// </summary>
        /// <param name="index">Index of location.</param>
        /// <returns>A tuple containing the index of the location and an array of the data.</returns>
        public Tuple<int, object[]> this[int index] => new Tuple<int, object[]>(index, (from collection in Items select collection.ElementAt(index)).ToArray());
        
        /// <summary>
        /// Gets an object to enumerate over.
        /// </summary>
        /// <returns>The current object.</returns>
        public IEnumerator<Tuple<int, object[]>> GetEnumerator()
        {
            return this;
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return (IEnumerator)GetEnumerator();
        }


        int position = -1;

        /// <summary>
        /// The data at the current point in the itteration.
        /// </summary>
        public Tuple<int, object[]> Current => this[position];

        object IEnumerator.Current => Current;

        /// <summary>
        /// Releses any resources and disposes.
        /// </summary>
        public void Dispose() { }

        /// <summary>
        /// Attempts to move to the next position in the itteration.
        /// </summary>
        /// <returns>Boolean indicating wether the itteration can continue.</returns>
        public bool MoveNext()
        {
            position++;
            return (position < Count);
        }

        /// <summary>
        /// Resets the enumeration.
        /// </summary>
        public void Reset()
        {
            position = -1;
        }
    }

    /// <summary>
    /// Allows for itteration of multiple collections similtaniously. Generic version for simplified use if all collections hold the same data type.
    /// </summary>
    public class MultiItterator<T> : IEnumerable<Tuple<int, T[]>>, IEnumerator<Tuple<int, T[]>>
    {
        /// <summary>
        /// The collections being itterated over.
        /// </summary>
        public readonly ICollection<T>[] Items;

        /// <summary>
        /// The number of items in the contained collections.
        /// </summary>
        public int Count { get; protected set; }

        /// <summary>
        /// Creates a new instance of the MultiItterator class. Collections must have the same length.
        /// </summary>
        /// <param name="items">IColections of objects.</param>
        public MultiItterator(params ICollection<T>[] items)
        {
            bool sameLength = true;
            for (int i = 1; i < items.Length; i++)
            {
                if (items[i].Count != items[0].Count)
                {
                    sameLength = false;
                    break;
                }
            }

            if (sameLength)
            {
                Items = items;
                Count = Items[0].Count;
            }
            else
            {
                throw new ArgumentException("The colections provided were not all of the same length.");
            }
        }


        /// <summary>
        /// Returns the index and data at the specified index in the collections.
        /// </summary>
        /// <param name="index">Index of location.</param>
        /// <returns>A tuple containing the index of the location and an array of the data.</returns>
        public Tuple<int, T[]> this[int index] => new Tuple<int, T[]>(index, (from collection in Items select collection.ElementAt(index)).ToArray());

        /// <summary>
        /// Gets an object to enumerate over.
        /// </summary>
        /// <returns>The current object.</returns>
        public IEnumerator<Tuple<int, T[]>> GetEnumerator()
        {
            return this;
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return (IEnumerator)GetEnumerator();
        }


        int position = -1;

        /// <summary>
        /// The data at the current point in the itteration.
        /// </summary>
        public Tuple<int, T[]> Current => this[position];

        object IEnumerator.Current => Current;

        /// <summary>
        /// Releses any resources and disposes.
        /// </summary>
        public void Dispose() { }

        /// <summary>
        /// Attempts to move to the next position in the itteration.
        /// </summary>
        /// <returns>Boolean indicating wether the itteration can continue.</returns>
        public bool MoveNext()
        {
            position++;
            return (position < Count);
        }

        /// <summary>
        /// Resets the enumeration.
        /// </summary>
        public void Reset()
        {
            position = -1;
        }
    }
}