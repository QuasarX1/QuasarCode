﻿using System;
using System.Collections.Generic;
using System.Text;

using System.IO;
using System.Windows.Input;

namespace QuasarCode.Library.IO.Text
{
    /// <summary>
    /// Provites IO methods for intervacing with a text based console.
    /// </summary>
    public class Console: IConsole
    {
        public bool IsInputRedirected { get; protected set; }
        protected TextWriter error;
        public TextWriter Error { get { return this.error; } protected set { this.error = value; } }
        protected TextReader input;
        public TextReader In { get { return this.input; } protected set { this.input = value; } }
        public bool IsErrorRedirected { get; protected set; }
        public bool IsOutputRedirected { get; protected set; }
        protected TextWriter output;
        public TextWriter Out { get { return this.output; } protected set { this.output = value; } }
        public string Title { get; set; }
        public bool ErrorDefultsToOutput { get; protected set; }



        public event EventHandler OnWrite;
        public event EventHandler OnRead;
        public event EventHandler OnClear;

        public Console(string title = "Console", TextReader inputReader = null, TextWriter outputWriter = null, TextWriter errorWriter = null, bool errorDefultsToOutput = false)
        {
            this.Title = title;

            this.ErrorDefultsToOutput = errorDefultsToOutput;

            this.SetIn(inputReader);

            this.SetOut(outputWriter);

            this.SetError(errorWriter);
        }

        public void Clear()
        {
            OnClear?.Invoke(this, new EventArgs());
        }

        public int Read()
        {
            int result = this.In.Read();
            OnRead?.Invoke(this, new EventArgs());
            return result;
        }

        public string ReadKey(ref EventHandler<string> keyPressEvent, bool intercept = false)
        {
            string value = Console.ReadKey(ref keyPressEvent);
            if (!intercept)
            {
                Console.Print(value);
            }
            return value;
        }

        public string ReadLine()
        {
            string result = this.In.ReadLine();
            OnRead?.Invoke(this, new EventArgs());
            return result;
        }

        public void SetError(TextWriter newError = null)
        {
            if (newError != null)
            {
                this.error = newError;
                this.IsErrorRedirected = this.error != System.Console.Error;
            }
            else if (this.ErrorDefultsToOutput)
            {
                this.error = this.output;
                this.IsErrorRedirected = this.error != System.Console.Error;
            }
            else {
                this.error = System.Console.Error;
                this.IsErrorRedirected = false;
            }
        }

        public void SetIn(TextReader newIn = null)
        {
            if (newIn != null)
            {
                this.input = newIn;
                this.IsInputRedirected = this.input != System.Console.In;
            }
            else
            {
                this.input = System.Console.In;
                this.IsInputRedirected = false;
            }
        }

        public void SetOut(TextWriter newOut = null)
        {
            if (newOut != null)
            {
                this.output = newOut;
                this.IsOutputRedirected = this.output != System.Console.Out;
            }
            else
            {
                this.output = System.Console.Out;
                this.IsOutputRedirected = false;
            }
        }

        public void Write(ulong value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(bool value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(char value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(char[] buffer) { string value = ""; foreach (char character in buffer) { value += character; } Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(char[] buffer, int index, int count) { string value = ""; for (int i = index; i < index + count; i++) { value += buffer[i]; } Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(double value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(long value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(object value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(float value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(string value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(string format, object arg0) { Console.Print(string.Format(format, arg0), ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(string format, object arg0, object arg1) { Console.Print(string.Format(format, arg0, arg1), ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(string format, object arg0, object arg1, object arg2) { Console.Print(string.Format(format, arg0, arg1, arg2), ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(string format, params object[] arg) { Console.Print(string.Format(format, args: arg), ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(uint value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(decimal value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }
        public void Write(int value) { Console.Print(value, ref this.output, end: ""); OnWrite?.Invoke(this, new EventArgs()); }

        public void WriteLine(ulong value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine() { Console.Print(output: ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(bool value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(char[] buffer) { string value = ""; foreach (char character in buffer) { value += character; } Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(char[] buffer, int index, int count) { string value = ""; for (int i = index; i < index + count; i++) { value += buffer[i]; } Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(decimal value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(double value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(uint value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(int value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(object value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(float value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(string value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(string format, object arg0) { Console.Print(string.Format(format, arg0), ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(string format, object arg0, object arg1) { Console.Print(string.Format(format, arg0, arg1), ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(string format, object arg0, object arg1, object arg2) { Console.Print(string.Format(format, arg0, arg1, arg2), ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(string format, params object[] arg) { Console.Print(string.Format(format, args: arg), ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(long value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }
        public void WriteLine(char value) { Console.Print(value, ref this.output); OnWrite?.Invoke(this, new EventArgs()); }


        public TextReader GetIn()
        {
            return this.input;
        }

        public TextWriter GetOut()
        {
            return this.output;
        }

        public TextWriter GetError()
        {
            return this.error;
        }







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
        /// </summary>
        public static void Print()
        {
            Print(ref DeafultOut);
        }

        /// <summary>
        /// Outputs text to the console. Prints only a new line.
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// </summary>
        public static void Print(ref System.IO.TextWriter output)
        {
            output.WriteLine();
        }

        /// <summary>
        /// Outputs text to the console.
        /// </summary>
        /// <param name="text">The text to output.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="moreText">List of any other strings to output.</param>
        public static void Print(string text, string end = "\n", params string[] moreText)
        {
            Print(text, ref DeafultOut, end, moreText);
        }

        /// <summary>
        /// Outputs text to the console.
        /// </summary>
        /// <param name="text">The text to output.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="moreText">List of any other strings to output.</param>
        public static void Print(string text, ref System.IO.TextWriter output, string end = "\n", params string[] moreText)
        {
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
        /// <param name="moreText">List of any other strings to output. Must be able to be implicitly converted to a string.</param>
        public static void Print(object text, string end = "\n", params object[] moreText)
        {
            Print(text, ref DeafultOut, end, moreText);
        }

        /// <summary>
        /// Outputs text versions of objects to the console.
        /// </summary>
        /// <param name="text">The object to output. Must be able to be implicitly converted to a string.</param>
        /// <param name="end">String added to the end of the output.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="moreText">List of any other strings to output. Must be able to be implicitly converted to a string.</param>
        public static void Print(object text, ref System.IO.TextWriter output, string end = "\n", params object[] moreText)
        {
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
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string indicator = ">>> ")
        {
            return Input(ref DeafultOut, ref DeafultIn, indicator);
        }

        /// <summary>
        /// Retrives an input from the console.
        /// </summary>
        /// <param name="indicator">String to format line for input.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(ref System.IO.TextWriter output, ref System.IO.TextReader input, string indicator = ">>> ")
        {
            output.Write(indicator);

            return input.ReadLine();
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message.
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string prompt, string indicator = "\n>>> ")
        {
            return Input(ref DeafultOut, ref DeafultIn, prompt, indicator);
        }

        /// <summary>
        /// Retrives an input from the console with a prompt message.
        /// </summary>
        /// <param name="prompt">Message to be printed to the display to request input.</param>
        /// <param name="indicator">String to format line for input.</param>
        /// <param name="output">Alternitive output stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultOut</param>
        /// <param name="input">Alternitive input stream. Deafults to QuasarCode.Library.IO.Text.Console.DeafultIn</param>
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(ref System.IO.TextWriter output, ref System.IO.TextReader input, string prompt, string indicator = "\n>>> ")
        {
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
        /// <returns>A line of input from the console as a string.</returns>
        public static string Input(string prompt, Func<string, bool> validator, string errorMessage, string indicator = "\n>>> ")
        {
            return Input(ref DeafultOut, ref DeafultIn, prompt, validator, errorMessage, indicator);
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
        public static string Input(ref System.IO.TextWriter output, ref System.IO.TextReader input, string prompt, Func<string, bool> validator, string errorMessage, string indicator = "\n>>> ")
        {
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
        /// <returns>A line of input from the console, coverted to the specified type.</returns>
        public static T Input<T>(string prompt, Func<string, T> converter, string indicator = "\n>>> ")
        {
            return Input(ref DeafultOut, ref DeafultIn, prompt, converter, indicator);
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
        public static T Input<T>(ref System.IO.TextWriter output, ref System.IO.TextReader input, string prompt, Func<string, T> converter, string indicator = "\n>>> ")
        {
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
        /// <returns>A line of input from the console, coverted to the specified type.</returns>
        public static T Input<T>(string prompt, Func<string, T> converter, Func<object, bool> validator, string errorMessage, string indicator = "\n>>> ")
        {
            return Input(ref DeafultOut, ref DeafultIn, prompt, converter, validator, errorMessage, indicator);
        }

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
        public static T Input<T>(ref System.IO.TextWriter output, ref System.IO.TextReader input, string prompt, Func<string, T> converter, Func<object, bool> validator, string errorMessage, string indicator = "\n>>> ")
        {
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
        /// Allows the user to select an item from an array of options. Returns the option. Uses the DeafultOut stream.
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
                DeafultOut.WriteLine(message);
            }

            int index = 0;
            int i;
            while (true)
            {
                i = 0;
                for (i = 0; i < 8; i++)
                {
                    DeafultOut.WriteLine((i + 1) + ".) " + options[index + i]);

                    if (index + i + 1 == options.Length)
                    {
                        i++;
                        break;
                    }
                }

                if (options.Length > 8)
                {
                    DeafultOut.WriteLine("9.) Next Page");
                }

                string result;
                result = Convert.ToString(System.Console.ReadKey(!displayInput).KeyChar);

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
                        DeafultOut.WriteLine("Invalid selection - the number selected was out of range. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                    }
                }
                else
                {
                    DeafultOut.WriteLine("Invalid selection - the selection was not a number. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                }
            }
        }

        /// <summary>
        /// Allows the user to select an item from an array of options. Returns the option's index. Uses the DeafultOut stream.
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
                DeafultOut.WriteLine(message);
            }

            int index = 0;
            int i;
            while (true)
            {
                i = 0;
                for (i = 0; i < 8; i++)
                {
                    DeafultOut.WriteLine((i + 1) + ".) " + options[index + i]);

                    if (index + i + 1 == options.Length)
                    {
                        i++;
                        break;
                    }
                }

                if (options.Length > 8)
                {
                    DeafultOut.WriteLine("9.) Next Page");
                }

                string result;
                result = Convert.ToString(System.Console.ReadKey(!displayInput).KeyChar);
                

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
                        DeafultOut.WriteLine("Invalid selection - the number selected was out of range. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                    }
                }
                else
                {
                    DeafultOut.WriteLine("Invalid selection - the selection was not a number. You must chose an option from 1 to {0}", (options.Length > 8) ? i + 1 : i);
                }
            }
        }

        /// <summary>
        /// Allows the user to select an item from an array of options. Returns the option. Uses a custom event for presenting characters for option selection.
        /// </summary>
        /// <typeparam name="T">Type of the objects in the array.</typeparam>
        /// <param name="options">Array of options to be selected from. Must have a length of at least 1.</param>
        /// <param name="message">Optional message to display to the user.</param>
        /// <param name="displayInput">Wether or not the user's selected option will be displayed on the console.</param>
        /// <param name="output">Alternitive output stream.</param>
        /// <param name="keyPressEvent">Event raised when an option is selected</param>
        /// <returns>Selected option.</returns>
        public static T Option<T>(T[] options, ref EventHandler<string> keyPressEvent, ref System.IO.TextWriter output, string message = null, bool displayInput = false)
        {
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
                result = ReadKey(ref keyPressEvent);

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
        /// Allows the user to select an item from an array of options. Returns the option's index. Uses a custom event for presenting characters for option selection.
        /// </summary>
        /// <param name="options">Array of options to be selected from. Must have a length of at least 1.</param>
        /// <param name="message">Optional message to display to the user.</param>
        /// <param name="displayInput">Wether or not the user's selected option will be displayed on the console.</param>
        /// <param name="output">Alternitive output stream.</param>
        /// <param name="keyPressEvent">Event raised when an option is selected</param>
        /// <returns>Index of selected option.</returns>
        public static int Option(object[] options, ref EventHandler<string> keyPressEvent, ref System.IO.TextWriter output, string message = null, bool displayInput = false)
        {
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
                result = ReadKey(ref keyPressEvent);


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
        public static string ReadKey(ref EventHandler<string> keyPressEvent)
        {
            KeyPressUpdater updater = new KeyPressUpdater();
            keyPressEvent += updater.onPress;

            // Block the calling thread untill a value is returned
            while (true)
            {
                if (updater.key != null)
                {
                    keyPressEvent -= updater.onPress;
                    break;
                }
            }
            
            return updater.key;
        }

        private class KeyPressUpdater
        {
            public string key = null;

            public KeyPressUpdater()
            {
                this.key = null;
            }

            public void onPress(object sender, string keyPressed)
            {
                key = keyPressed;
            }
        }
    }
    
}