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
        /// Defult text output stream. Deafults to System.Console.Out
        /// </summary>
        public static System.IO.TextWriter DeafultOut = System.Console.Out;

        /// <summary>
        /// Defult error stream. Deafults to System.Console.Error
        /// </summary>
        public static System.IO.TextWriter DeafultError = System.Console.Error;

        /// <summary>
        /// Defult text input stream. Deafults to System.Console.In
        /// </summary>
        public static System.IO.TextReader DeafultIn = System.Console.In;

        /// <summary>
        /// Outputs text to the console. Prints only a new line.
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// </summary>
        public static void Print(System.IO.TextWriter output = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            output.WriteLine();
        }

        /// <summary>
        /// Outputs text to the console.
        /// </summary>
        /// <param name="text">The text to output.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="moreText">List of any other strings to output.</param>
        public static void Print(string text, string end = "\n", System.IO.TextWriter output = null, params string[] moreText)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            output.Write(text);

            if (moreText != null)
            {
                output.Write(" ");
            }

            foreach (string item in moreText)
            {
                output.Write(item + " ");
            }

            output.Write(end);
        }

        /// <summary>
        /// Outputs text versions of objects to the console.
        /// </summary>
        /// <param name="text">The object to output. Must be able to be implicitly converted to a string.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="moreText">List of any other strings to output. Must be able to be implicitly converted to a string.</param>
        public static void Print(object text, string end = "\n", System.IO.TextWriter output = null, params object[] moreText)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            try
            {
                output.Write(Convert.ToString(text));

                if (moreText != null)
                {
                    output.Write(" ");
                }

                foreach (object item in moreText)
                {
                    output.Write(Convert.ToString(item) + " ");
                }

                output.Write(end);
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
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string indicator = ">>> ", System.IO.TextWriter output = null, System.IO.TextReader input = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (input is null)
            {
                input = DeafultIn;
            }

            output.Write(indicator);

            return input.ReadLine();
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message.
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string prompt, string indicator = "\n>>> ", System.IO.TextWriter output = null, System.IO.TextReader input = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (input is null)
            {
                input = DeafultIn;
            }

            output.Write(prompt + indicator);

            return input.ReadLine();
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message. Uses a method deligate to force valid input.
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="validator">Validator method deligate. Takes a string and returns a boolean.</param>
        /// <param name="errorMessage">Message to display if validation fails before asking for the input again.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string prompt, Func<string, bool> validator, string errorMessage, string indicator = "\n>>> ", System.IO.TextWriter output = null, System.IO.TextReader input = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (input is null)
            {
                input = DeafultIn;
            }

            string result;
            while (true)
            {
                output.Write(prompt + indicator);
                result = input.ReadLine();

                if (validator(result))
                {
                    break;
                }
                else
                {
                    output.WriteLine(errorMessage);
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
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console, coverted to the specified type.</returns>
        public static T Input<T>(string prompt, Func<string, T> converter, string indicator = "\n>>> ", System.IO.TextWriter output = null, System.IO.TextReader input = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (input is null)
            {
                input = DeafultIn;
            }

            output.Write(prompt + indicator);

            return converter(input.ReadLine());
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
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console, coverted to the specified type.</returns>
        public static T Input<T>(string prompt, Func<string, T> converter, Func<object, bool> validator, string errorMessage, string indicator = "\n>>> ", System.IO.TextWriter output = null, System.IO.TextReader input = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (input is null)
            {
                input = DeafultIn;
            }

            T result;
            while (true)
            {
                output.Write(prompt + indicator);
                result = converter(input.ReadLine());

                if (validator(result))
                {
                    break;
                }
                else
                {
                    output.WriteLine(errorMessage);
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
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="keyPressEvent">Event raised when an option is selected</param>
        /// <returns>Selected option.</returns>
        public static T Option<T>(T[] options, string message = null, bool displayInput = false, System.IO.TextWriter output = null, EventHandler<char> keyPressEvent = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (options.Length == 0)
            {
                throw new ArgumentException("No options were provided - the array was enpty.");
            }

            if (message != null)
            {
                output.WriteLine(message);
            }

            int index = 0;
            int i;
            while (true)
            {
                i = 0;
                for (i = 0; i < 8; i++)
                {
                    output.WriteLine((i + 1) + ".) " + options[index + i]);

                    if (index + i + 1 == options.Length)
                    {
                        i++;
                        break;
                    }
                }

                if (options.Length > 8)
                {
                    output.WriteLine("9.) Next Page");
                }

                string result;
                if (keyPressEvent is null)
                {
                    result = Convert.ToString(System.Console.ReadKey(!displayInput).KeyChar);
                }
                else
                {
                    result = Convert.ToString(ReadChar(keyPressEvent));
                }

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
                        output.WriteLine("Invalid selection - the number selected was out of range. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                    }
                }
                else
                {
                    output.WriteLine("Invalid selection - the selection was not a number. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                }
            }
        }

        /// <summary>
        /// Allows the user to select an item from an array of options. Returns the option's index.
        /// </summary>
        /// <param name="options">Array of options to be selected from. Must have a length of at least 1.</param>
        /// <param name="message">Optional message to display to the user.</param>
        /// <param name="displayInput">Wether or not the user's selected option will be displayed on the console.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="keyPressEvent">Event raised when an option is selected</param>
        /// <returns>Index of selected option.</returns>
        public static int Option(object[] options, string message = null, bool displayInput = false, System.IO.TextWriter output = null, EventHandler<char> keyPressEvent = null)
        {
            if (output is null)
            {
                output = DeafultOut;
            }

            if (options.Length == 0)
            {
                throw new ArgumentException("No options were provided - the array was enpty.");
            }

            if (message != null)
            {
                output.WriteLine(message);
            }

            int index = 0;
            int i;
            while (true)
            {
                i = 0;
                for (i = 0; i < 8; i++)
                {
                    output.WriteLine((i + 1) + ".) " + options[index + i]);

                    if (index + i + 1 == options.Length)
                    {
                        i++;
                        break;
                    }
                }

                if (options.Length > 8)
                {
                    output.WriteLine("9.) Next Page");
                }

                string result;
                if (keyPressEvent is null)
                {
                    result = Convert.ToString(System.Console.ReadKey(!displayInput).KeyChar);
                }
                else
                {
                    result = Convert.ToString(ReadChar(keyPressEvent));
                }
                

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
                        output.WriteLine("Invalid selection - the number selected was out of range. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                    }
                }
                else
                {
                    output.WriteLine("Invalid selection - the selection was not a number. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                }
            }
        }


        /// <summary>
        /// Emulates the System.Console.ReadKey method but takes an event that provides characters returns a char.
        /// </summary>
        /// <param name="keyPressEvent">Event that provides characters</param>
        /// <returns></returns>
        public static char ReadChar(EventHandler<char> keyPressEvent)
        {
            char? key = null;

            void onPress(object sender, char keyPressed)
            {
                keyPressEvent -= onPress;
                key = keyPressed;
            }

            keyPressEvent += onPress;

            // Block the calling thread untill a value is returned
            while (key is null)
            {
                break;
            }
            
            return (char)key;
            
        }
    }
}