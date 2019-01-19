using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Tools
{
    /// <summary>
    /// Provides type and content testing methods for testing objects.
    /// </summary>
    public static class Validators
    {
        /// <summary>
        /// Checks to see if the provided object can be converted to a boolean.
        /// </summary>
        /// <param name="testCase">The object to be tested.</param>
        /// <returns>Boolean</returns>
        public static bool IsBool(object testCase)
        {
            try
            {
                Convert.ToBoolean(testCase);
                return true;
            }
            catch (InvalidCastException)
            {
                return false;
            }
        }

        /// <summary>
        /// Checks to see if the provided object can be converted to a character.
        /// </summary>
        /// <param name="testCase">The object to be tested.</param>
        /// <returns>Boolean</returns>
        public static bool IsChar(object testCase)
        {
            try
            {
                Convert.ToChar(testCase);
                return true;
            }
            catch (InvalidCastException)
            {
                return false;
            }
        }

        /// <summary>
        /// Checks to see if the provided object can be converted to a string.
        /// </summary>
        /// <param name="testCase">The object to be tested.</param>
        /// <returns>Boolean</returns>
        public static bool IsString(object testCase)
        {
            try
            {
                Convert.ToString(testCase);
                return true;
            }
            catch (InvalidCastException)
            {
                return false;
            }
        }

        /// <summary>
        /// Checks to see if the provided character is an alpha character.
        /// </summary>
        /// <param name="testCase">Character to test.</param>
        /// <returns>Boolean</returns>
        public static bool IsAlpha(char testCase)
        {
            throw new NotImplementedException();
        }

        /// <summary>
        /// Checks to see if the provided string contains only alpha character.
        /// </summary>
        /// <param name="testCase">String to test.</param>
        /// <returns>Boolean</returns>
        public static bool IsAlpha(string testCase)
        {
            throw new NotImplementedException();
        }

        /// <summary>
        /// Checks to see if the provided object is a valid character or string and contains only alpha characters.
        /// </summary>
        /// <param name="testCase">Object to test.</param>
        /// <returns>Boolean - false if not a character or string or has no conversion to one</returns>
        public static bool IsAlpha(object testCase)
        {
            if (IsChar(testCase))
            {
                return IsAlpha(Convert.ToChar(testCase));
            }
            else if (IsString(testCase))
            {
                return IsAlpha(Convert.ToString(testCase));
            }
            else
            {
                return false;
            }
        }

        /// <summary>
        /// Checks to see if the provided object can be converted to an integer (int64).
        /// </summary>
        /// <param name="testCase">The object to be tested.</param>
        /// <returns>Boolean</returns>
        public static bool IsInt(object testCase)
        {
            try
            {
                Convert.ToInt64(testCase);
                return true;
            }
            catch (InvalidCastException)
            {
                return false;
            }
        }

        /// <summary>
        /// Checks to see if the provided object can be converted to a float.
        /// </summary>
        /// <param name="testCase">The object to be tested.</param>
        /// <returns>Boolean</returns>
        public static bool IsDouble(object testCase)
        {
            try
            {
                Convert.ToDouble(testCase);
                return true;
            }
            catch (InvalidCastException)
            {
                return false;
            }
        }
    }
}
