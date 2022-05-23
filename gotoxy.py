# Cross-platform gotoxy functions.
__author__ = "Frank Cedano <frankcedano64@gmail.com>"
__version__ = "0.2"

__all__ = [
    "GetCursorPosition", "SetCursorPosition", "GetTerminalSize",
    "SetTerminalSize"]

from os import get_terminal_size
from sys import platform

if platform.startswith("win32"):
    from ctypes import POINTER, Structure, WinDLL, byref, c_bool, c_void_p
    from ctypes.wintypes import (
        _COORD, DWORD, HANDLE, HLOCAL, LPWSTR, SMALL_RECT, WORD)

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        _fields_ = [
            ("dwSize", _COORD),
            ("dwCursorPosition", _COORD),
            ("wAttributes", WORD),
            ("srWindow", SMALL_RECT),
            ("dwMaximumWindowSize", _COORD)
        ]

    # Windows functions
    kernel32 = WinDLL("kernel32")

    GetLastError = kernel32.GetLastError
    FormatMessage = kernel32.FormatMessageW
    LocalFree = kernel32.LocalFree

    GetStdHandle = kernel32.GetStdHandle
    GetConsoleScreenBufferInfo = kernel32.GetConsoleScreenBufferInfo
    SetConsoleCursorPosition = kernel32.SetConsoleCursorPosition
    SetConsoleWindowInfo = kernel32.SetConsoleWindowInfo

    # Specification of arguments and return values.
    GetLastError.restype = DWORD

    FormatMessage.argtypes = (
        DWORD, c_void_p, DWORD, DWORD, LPWSTR, DWORD, c_void_p)
    FormatMessage.restype = DWORD

    LocalFree.argtypes = (HLOCAL,)
    LocalFree.restype = HLOCAL

    GetStdHandle.argtypes = (DWORD,)
    GetStdHandle.restype = HANDLE

    GetConsoleScreenBufferInfo.argtypes = (
        HANDLE, POINTER(CONSOLE_SCREEN_BUFFER_INFO))
    GetConsoleScreenBufferInfo.restype = c_bool

    SetConsoleCursorPosition.argtypes = (HANDLE, _COORD)
    SetConsoleCursorPosition.restype = c_bool

    SetConsoleWindowInfo.argtypes = (HANDLE, c_bool, POINTER(SMALL_RECT))
    SetConsoleWindowInfo.restype = c_bool

    # Constants
    STDOUT = GetStdHandle(-11)

    # Functions
    def _GetMessageError():
        errorcode = GetLastError()
        if errorcode == 0: return "Unknown error."

        from ctypes import cast

        def MAKELANGID(primary: int, sublang: int) -> int:
            # Gets the user's language code.
            return (primary & 0xFF) | (sublang & 0xFF) << 16

        message = LPWSTR()

        out_FM = FormatMessage(
            0x00000100 | 0x00001000 | 0x00000200,
            None, errorcode, MAKELANGID(0x00, 0x01),
            cast(byref(message), LPWSTR), 0, None)

        if out_FM == 0: return None

        out = message.value
        LocalFree(message)

        return out.strip()

else:
    from ctypes import POINTER, CDLL, byref, c_char_p, c_int, c_ushort
    from os.path import abspath, dirname, sep
    from re import match

    if __file__ != "":
        exec_path = dirname(abspath(__file__))
    else:
        from sys import argv
        exec_path = dirname(abspath(argv[0]))

    try:
        gotoxy_so = CDLL(f"{exec_path}{sep}_gotoxy.so")
        gotoxy_so.GetCursorPosition.restype = c_char_p
        gotoxy_so.GetCursorPosition.argtypes = (POINTER(c_int),)
        gotoxy_so.SetTerminalSize.restype = c_char_p
        gotoxy_so.SetTerminalSize.argtypes = (c_ushort, c_ushort)

    except OSError:
        raise FileNotFoundError('The file "_gotoxy.so" is not found.')

def GetCursorPosition() -> tuple:
    """Gets the current cursor position.
    """
    if platform.startswith("win32"):
        out = CONSOLE_SCREEN_BUFFER_INFO()

        if GetConsoleScreenBufferInfo(STDOUT, byref(out)):
            return (out.dwCursorPosition.X, out.dwCursorPosition.Y)
        else:
            raise OSError(_GetMessageError())

    elif platform.startswith("linux"):
        code = c_int()
        out = gotoxy_so.GetCursorPosition(byref(code)).decode("utf-8")

        if code.value == 0: raise OSError(out)

        try:
            matches = match(r"\x1b\[(\d*);(\d*)R", out)
            groups = matches.groups()
            return (int(groups[1]) - 1, int(groups[0]) - 1)

        except AttributeError:
            return (0, 0)

def SetCursorPosition(x: int, y: int):
    """Sets the cursor position at the specified coordinates.
    """
    if (not type(x) == int) or (not type(y) == int):
        raise TypeError("Arguments must be integers.")
    elif (x < 0) or (y < 0):
        raise ValueError("Arguments must be positive integers.")
    elif (platform.startswith("win32")) and ((x > 32767) or (y > 32767)):
        raise ValueError("Arguments must have a value no greater than 32767.")
    elif (x > 65535) or (y > 65535):
        raise ValueError("Arguments must have a value no greater than 65535.")

    if platform.startswith("win32"):
        if not SetConsoleCursorPosition(STDOUT, _COORD(x, y)):
            raise OSError(_GetMessageError())

    elif platform.startswith("linux"):
        # To evaluate whether it is possible to position the cursor.
        GetCursorPosition()

        print("\x1B[%d;%df" % (y + 1, x + 1), end='')

def GetTerminalSize() -> tuple:
    """Gets the current buffer size from the console.
    """
    return get_terminal_size()[0:2]

def SetTerminalSize(columns: int, lines: int):
    """Sets the console buffer size. Attempting to change the number of lines
    may have no effect.
    """
    if (not type(columns) == int) or (not type(lines) == int):
        raise TypeError("Arguments must be integers.")
    elif (columns < 0) or (lines < 0):
        raise ValueError("Arguments must be positive integers.")
    elif (platform.startswith("win32")) and ((columns > 32767) or (lines > 32767)):
        raise ValueError("Arguments must have a value no greater than 32767.")
    elif (columns > 65535) or (lines > 65535):
        raise ValueError("Arguments must have a value no greater than 65535.")

    if platform.startswith("win32"):
        if not SetConsoleWindowInfo(
                STDOUT, False, byref(SMALL_RECT(0, 0, columns, lines))):
            raise OSError(_GetMessageError())

    else:
        result = gotoxy_so.SetTerminalSize(columns, lines).decode("utf-8")
        if result != "none": raise OSError(result)
