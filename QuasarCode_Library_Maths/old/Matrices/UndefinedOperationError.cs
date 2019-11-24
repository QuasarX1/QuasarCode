using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.Maths.old.Matrices
{
    public class UndefinedOperationException : InvalidOperationException
    {
        public UndefinedOperationException() : base("The state of the object means that this operation is undefined.") { }

        public UndefinedOperationException(string message) : base(message) { }

        public UndefinedOperationException(string message, Exception innerException) : base(message, innerException) { }

        public UndefinedOperationException(System.Runtime.Serialization.SerializationInfo info, System.Runtime.Serialization.StreamingContext context) : base(info, context) { }
    }
}