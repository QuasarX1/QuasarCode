using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.IO.Text
{
    /// <summary>
    /// 
    /// </summary>
    public class Console
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

            if (moreText != null)
            {
                System.Console.Write(" ");
            }

            foreach (string item in moreText)
            {
                System.Console.Write(item + " ");
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
                System.Console.Write(Convert.ToString(text));

                if (moreText != null)
                {
                    System.Console.Write(" ");
                }

                foreach (object item in moreText)
                {
                    System.Console.Write(Convert.ToString(item) + " ");
                }

                System.Console.Write(end);
            }
            catch (InvalidCastException e)
            {
                throw new InvalidCastException("Could not implicitly convert an object to string.", e);
            }
        }
        
        
        /// <summary>
        /// Retrives an input from the console.
        /// </summary>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns></returns>
        public static string Input(string indicator = ">>> ")
        {
            System.Console.Write(indicator);

            return System.Console.ReadLine();
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message.
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns></returns>
        public static string Input(string prompt, string indicator = "\n>>> ")
        {
            System.Console.Write(prompt + indicator);

            return System.Console.ReadLine();
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message. Converts the input to the given type.
        /// </summary>
        /// <typeparam name="T">Return type</typeparam>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="converter">Method deligate to convert the string input to the requested type.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns></returns>
        public static T Input<T>(string prompt, Func<string, T> converter, string indicator = "\n>>> ")
        {
            System.Console.Write(prompt + indicator);

            return converter(System.Console.ReadLine());
        }
    }
}
