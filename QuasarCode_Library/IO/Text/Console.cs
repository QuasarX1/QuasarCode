using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.IO.Text
{
    /// <summary>
    /// Provites IO methods for intervacing with a text based console.
    /// </summary>
    public static class Console
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
        /// <returns>A line of input from the console as a string.</returns>
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
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string prompt, string indicator = "\n>>> ")
        {
            System.Console.Write(prompt + indicator);

            return System.Console.ReadLine();
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message. Uses a method deligate to force valid input.
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="validator">Validator method deligate. Takes a string and returns a boolean.</param>
        /// <param name="errorMessage">Message to display if validation fails before asking for the input again.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string prompt, Func<string, bool> validator, string errorMessage, string indicator = "\n>>> ")
        {
            string result;
            while (true)
            {
                System.Console.Write(prompt + indicator);
                result = System.Console.ReadLine();

                if (validator(result))
                {
                    break;
                }
                else
                {
                    System.Console.WriteLine(errorMessage);
                }
            }
            

            return result;
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message. Converts the input to the given type.
        /// </summary>
        /// <typeparam name="T">Return type</typeparam>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="converter">Method deligate to convert the string input to the requested type.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns>A line of input from the console, coverted to the specified type.</returns>
        public static T Input<T>(string prompt, Func<string, T> converter, string indicator = "\n>>> ")
        {
            System.Console.Write(prompt + indicator);

            return converter(System.Console.ReadLine());
        }

        ///// <summary>
        ///// Retrives an input from the console with a prompt message. Uses a method deligate to force valid input. Converts the input to the given type (after validation).
        ///// </summary>
        ///// <param name="prompt">Message to be printed to the display to request input.</param>
        ///// <param name="validator">Validator method deligate. Takes a string and returns a boolean.</param>
        ///// <param name="errorMessage">Message to display if validation fails before asking for the input again.</param>
        ///// <param name="converter">Method deligate to convert the string input to the requested type.</param>
        ///// <param name="indicator">String to format line for input.</param>
        ///// <returns>A line of input from the console, coverted to the specified type.</returns>
        //public static T Input<T>(string prompt, Func<string, bool> validator, string errorMessage, Func<string, T> converter, string indicator = "\n>>> ")
        //{
        //    string result;
        //    while (true)
        //    {
        //        System.Console.Write(prompt + indicator);
        //        result = System.Console.ReadLine();

        //        if (validator(result))
        //        {
        //            break;
        //        }
        //        else
        //        {
        //            System.Console.WriteLine(errorMessage);
        //        }
        //    }


        //    return converter(result);
        //}

        /// <summary>
        /// Retrives an input from the console with a prompt message. Uses a method deligate to force valid input. Converts the input to the given type (before validation)
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="converter">Method deligate to convert the string input to the requested type.</param>
        /// <param name="validator">Validator method deligate. Takes an object of the specified type and returns a boolean.</param>
        /// <param name="errorMessage">Message to display if validation fails before asking for the input again.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns>A line of input from the console, coverted to the specified type.</returns>
        public static T Input<T>(string prompt, Func<string, T> converter, Func<object, bool> validator, string errorMessage, string indicator = "\n>>> ")
        {
            T result;
            while (true)
            {
                System.Console.Write(prompt + indicator);
                result = converter(System.Console.ReadLine());

                if (validator(result))
                {
                    break;
                }
                else
                {
                    System.Console.WriteLine(errorMessage);
                }
            }


            return result;
        }


        /// <summary>
        /// Allows the user to select an item from an array of options. Returns the option.
        /// </summary>
        /// <typeparam name="T">Type of the objects in the array.</typeparam>
        /// <param name="options">Array of options to be selected from. Must have a length of at least 1.</param>
        /// <param name="message">Optional message to display to the user.</param>
        /// <param name="displayInput">Wether or not the user's selected option will be displayed on the console.</param>
        /// <returns>Selected option.</returns>
        public static T Option<T>(T[] options, string message = null, bool displayInput = false)
        {
            if (options.Length == 0)
            {
                throw new ArgumentException("No options were provided - the array was enpty.");
            }

            if (message != null)
            {
                System.Console.WriteLine(message);
            }

            int index = 0;
            int i;
            while (true)
            {
                i = 0;
                for (i = 0; i < 8; i++)
                {
                    System.Console.WriteLine((i + 1) + ".) " + options[index + i]);

                    if (index + i + 1 == options.Length)
                    {
                        i++;
                        break;
                    }
                }

                if (options.Length > 8)
                {
                    System.Console.WriteLine("9.) Next Page");
                }

                string result = Convert.ToString(System.Console.ReadKey(!displayInput).KeyChar);

                if (Tools.Validators.IsInt(result))
                {
                    int resultnumber = Convert.ToInt32(result);
                    if (resultnumber <= i)
                    {
                        return options[index + resultnumber - 1];
                    }
                    else if (options.Length > 8 && resultnumber == 9)
                    {
                        index += i;
                        if (index + 1 == options.Length)
                        {
                            index = 0;
                        }
                    }
                    else
                    {
                        System.Console.WriteLine("Invalid selection - the number selected was out of range. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                    }
                }
                else
                {
                    System.Console.WriteLine("Invalid selection - the selection was not a number. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                }
            }
        }

        /// <summary>
        /// Allows the user to select an item from an array of options. Returns the option's index.
        /// </summary>
        /// <param name="options">Array of options to be selected from. Must have a length of at least 1.</param>
        /// <param name="message">Optional message to display to the user.</param>
        /// <param name="displayInput">Wether or not the user's selected option will be displayed on the console.</param>
        /// <returns>Index of selected option.</returns>
        public static int Option(object[] options, string message = null, bool displayInput = false)
        {
            if (options.Length == 0)
            {
                throw new ArgumentException("No options were provided - the array was enpty.");
            }

            if (message != null)
            {
                System.Console.WriteLine(message);
            }

            int index = 0;
            int i;
            while (true)
            {
                i = 0;
                for (i = 0; i < 8; i++)
                {
                    System.Console.WriteLine((i + 1) + ".) " + options[index + i]);

                    if (index + i + 1 == options.Length)
                    {
                        i++;
                        break;
                    }
                }

                if (options.Length > 8)
                {
                    System.Console.WriteLine("9.) Next Page");
                }

                string result = Convert.ToString(System.Console.ReadKey(!displayInput).KeyChar);

                if (Tools.Validators.IsInt(result))
                {
                    int resultnumber = Convert.ToInt32(result);
                    if (resultnumber <= i)
                    {
                        return index + resultnumber - 1;
                    }
                    else if (options.Length > 8 && resultnumber == 9)
                    {
                        index += i;
                        if (index + 1 == options.Length)
                        {
                            index = 0;
                        }
                    }
                    else
                    {
                        System.Console.WriteLine("Invalid selection - the number selected was out of range. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                    }
                }
                else
                {
                    System.Console.WriteLine("Invalid selection - the selection was not a number. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                }
            }
        }
    }
}
