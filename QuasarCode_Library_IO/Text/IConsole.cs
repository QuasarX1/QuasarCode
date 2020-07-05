using System;
using System.Collections.Generic;
using System.Text;

using System.IO;

namespace QuasarCode.Library.IO.Text
{
    public interface IConsole
    {
        bool IsInputRedirected { get; }
        TextWriter Error { get; }
        TextReader In { get; }
        bool IsErrorRedirected { get; }
        bool IsOutputRedirected { get; }
        TextWriter Out { get; }
        string Title { get; set; }

        event EventHandler OnWrite;
        event EventHandler OnRead;
        event EventHandler OnClear;


        TextReader GetIn();
        TextWriter GetOut();
        TextWriter GetError();


        void Clear();
        int Read();
        string ReadKey(ref EventHandler<string> keyPressEvent, bool intercept = false);
        string ReadLine();
        void SetError(TextWriter newError);
        void SetIn(TextReader newIn);
        void SetOut(TextWriter newOut);
        void Write(ulong value);
        void Write(bool value);
        void Write(char value);
        void Write(char[] buffer);
        void Write(char[] buffer, int index, int count);
        void Write(double value);
        void Write(long value);
        void Write(object value);
        void Write(float value);
        void Write(string value);
        void Write(string format, object arg0);
        void Write(string format, object arg0, object arg1);
        void Write(string format, object arg0, object arg1, object arg2);
        void Write(string format, params object[] arg);
        void Write(uint value);
        void Write(decimal value);
        void Write(int value);
        void WriteLine(ulong value);
        void WriteLine(string format, params object[] arg);
        void WriteLine();
        void WriteLine(bool value);
        void WriteLine(char[] buffer);
        void WriteLine(char[] buffer, int index, int count);
        void WriteLine(decimal value);
        void WriteLine(double value);
        void WriteLine(uint value);
        void WriteLine(int value);
        void WriteLine(object value);
        void WriteLine(float value);
        void WriteLine(string value);
        void WriteLine(string format, object arg0);
        void WriteLine(string format, object arg0, object arg1);
        void WriteLine(string format, object arg0, object arg1, object arg2);
        void WriteLine(long value);
        void WriteLine(char value);
    }
}
