using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.IO.Text
{
    /// <summary>
    /// 
    /// </summary>
    class Console
    {
        /// <summary>
        /// Outputs text to the console. Prints only a new line.
        /// </summary>
        public static void Print()
        {
            System.Console.WriteLine();
        }

        /// <summary>
        /// Outputs text to the console.
        /// </summary>
        /// <param name="text">The text to output.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="moreText">List of any other strings to output.</param>
        public static void Print(string text, string end = "\n", params string[] moreText)
        {
            System.Console.Write(text);

            foreach (string item in moreText)
            {
                System.Console.Write(item);
            }

            System.Console.Write(end);
        }

        /// <summary>
        /// Outputs text versions of objects to the console.
        /// </summary>
        /// <param name="text">The object to output. Must be able to be implicitly converted to a string.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="moreText">List of any other strings to output. Must be able to be implicitly converted to a string.</param>
        public static void Print(object text, string end = "\n", params object[] moreText)
        {
            try
            {
                System.Console.Write(text);

                foreach (string item in moreText)
                {
                    System.Console.Write(item);
                }

                System.Console.Write(end);
            }
            catch (InvalidCastException e)
            {
                throw new InvalidCastException("Could not implicitly convert an object to string.", e);
            }
        }
    }
}
