using System;
using System.Collections.Generic;
using System.Text;

namespace QuasarCode.Library.IO.Text
{
    public interface IWindowedConsole: IConsole
    {
        ConsoleColor ForegroundColor { get; set; }
        int WindowWidth { get; set; }
        int LargestWindowHeight { get; }
        int LargestWindowWidth { get; }
        bool CursorVisible { get; set; }
        bool CapsLock { get; }
        bool NumberLock { get; }
        bool TreatControlCAsInput { get; set; }
        int WindowHeight { get; set; }
        int WindowLeft { get; set; }
        int WindowTop { get; set; }
        ConsoleColor BackgroundColor { get; set; }

        event ConsoleCancelEventHandler CancelKeyPress;

        void Beep();
        void Beep(int frequency, int duration);
        void ResetColor();
        string ReadKey(bool intercept);
        string ReadKey();
        void SetWindowPosition(int left, int top);
        void SetWindowSize(int width, int height);
    }
}
