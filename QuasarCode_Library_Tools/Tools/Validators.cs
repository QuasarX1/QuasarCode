using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

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
            catch (FormatException)
            {
                return false;
            }
        }

        /// <summary>
        /// Checks to see if the provided object is a character object or a string with a single character.
        /// </summary>
        /// <param name="testCase">The object to be tested.</param>
        /// <returns>Boolean</returns>
        public static bool IsChar(object testCase)
        {
            return testCase.GetType() == typeof(char) || testCase.GetType() == typeof(string) && ((string)testCase).Length == 1;
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
            catch (FormatException)
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
            return Regex.IsMatch(Convert.ToString(testCase), @"^[\p{L}_']{1}$");
        }

        /// <summary>
        /// Checks to see if the provided string contains only alpha character.
        /// </summary>
        /// <param name="testCase">String to test.</param>
        /// <returns>Boolean</returns>
        public static bool IsAlpha(string testCase)
        {
            return Regex.IsMatch(testCase, @"^[\p{L}_']+$");
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
                Convert.ToInt32(testCase);

                try
                {
                    return Convert.ToDouble(Convert.ToInt32(testCase)) == Convert.ToDouble(testCase);
                }
                catch (InvalidCastException)
                {
                    return true;
                }
                catch (FormatException)
                {
                    return true;
                }
            }
            catch (InvalidCastException)
            {
                return false;
            }
            catch (FormatException)
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
            catch (FormatException)
            {
                return false;
            }
        }
        

        /// <summary>
        /// Tests if a number lies in the range lower (inclusive) to upper (exclusive) or outside the range if requested.
        /// </summary>
        /// <param name="testCase">Number to be tested.</param>
        /// <param name="lower">Lower boundry (inclusive).</param>
        /// <param name="upper">Upper boundry (exclusive).</param>
        /// <param name="inside">Specifies wether the test should be for lying inside the range (outside if false).</param>
        /// <returns>Boolean</returns>
        public static bool InRange(object testCase, double lower, double upper, bool inside = true)
        {
            if (IsDouble(testCase))
            {
                double value = Convert.ToDouble(testCase);
                if (upper != lower)
                {
                    if (lower <= value && value < upper)
                    {
                        return inside;
                    }
                    else
                    {
                        return !inside;
                    }
                }
                else// min == max
                {
                    throw new ArgumentException("The arguments for paramiters min and max are the same. They must be different as min is inclusive and max is exclusive.");
                }
                
            }
            else
            {
                throw new ArgumentException("The argument for paramiter testCase could not be converted to a double.");
            }
        }


        /// <summary>
        /// Tests if a given number is even.
        /// --| WARNING |-- Will ROUND floating point numbers to the nearest integer.
        /// </summary>
        /// <param name="testCase">The number to test. Must be convertable to an integer.</param>
        /// <returns>Boolean</returns>
        public static bool IsEven(object testCase)
        {
            if (IsDouble(testCase))
            {
                if (Convert.ToInt32(testCase) / 2.0 == (double)(Convert.ToInt32(testCase) / 2))
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                throw new ArgumentException("The argument for paramiter testCase could not be converted to an integer. Only integer values can be tested.");
            }
        }
    }
}
