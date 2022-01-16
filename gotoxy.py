# Cross-platform gotoxy functions.
__author__ = "Frank Cedano <frankcedano64@gmail.com>"
__version__ = "0.1"

__all__ = ["GetCursorPosition", "SetCursorPosition"]

from sys import platform

if platform.startswith("win32"):
    from ctypes import Structure, WinDLL, byref
    from ctypes.wintypes import _COORD, HANDLE, SMALL_RECT, WORD

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        _fields_ = [
            ("dwSize", _COORD),
            ("dwCursorPosition", _COORD),
            ("wAttributes", WORD),
            ("srWindow", SMALL_RECT),
            ("dwMaximumWindowSize", _COORD)
        ]

    kernel32 = WinDLL("kernel32")
    GetStdHandle = kernel32.GetStdHandle
    GetConsoleScreenBufferInfo = kernel32.GetConsoleScreenBufferInfo
    SetConsoleCursorPosition = kernel32.SetConsoleCursorPosition

    STDOUT = GetStdHandle(-11)

elif platform.startswith("linux"):
    import os, re, sys, termios, tty

else:
    raise Warning("There is no support for this system.")

def GetCursorPosition() -> tuple:
    if platform.startswith("win32"):
        out = CONSOLE_SCREEN_BUFFER_INFO()
        GetConsoleScreenBufferInfo(STDOUT, byref(out))
        return (out.dwCursorPosition.X, out.dwCursorPosition.Y)

    elif platform.startswith("linux"):
        # Thanks to netzego for the code.
        # https://stackoverflow.com/users/2787738/netzego
        buffer = ""
        stdin = sys.stdin.fileno()
        tattr = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()

            while True:
                buffer += sys.stdin.read(1)
                if buffer[-1] == "R": break

        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)

        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buffer)
            groups = matches.groups()
            return (int(groups[1])-1, int(groups[0])-1)

        except AttributeError: return (0, 0)

def SetCursorPosition(x: int, y: int):
    if (not type(x)==int) or (not type(y)==int):
        raise TypeError("The arguments x and y must be positive integers.")
    elif x<0 or y<0:
        raise ValueError("The arguments x and y must be positive integers.")

    if platform.startswith("win32"):
        SetConsoleCursorPosition(STDOUT, _COORD(x, y))

    elif platform.startswith("linux"):
        print("\x1B[%d;%df" % (y+1, x+1), end='')
