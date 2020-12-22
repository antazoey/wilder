using System;

namespace Wilder.Common.Exceptions
{
    public class FLParseException : Exception
    {
        private long StreamPosition { get; }

        public FLParseException(string message, long streamPosition) : base(message)
        {
            StreamPosition = streamPosition;
        }

        public FLParseException(string message, long streamPosition, Exception innerException) 
            : base(message, innerException)
        {
            StreamPosition = streamPosition;
        }
    }
}
