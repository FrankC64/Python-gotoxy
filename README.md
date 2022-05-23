# Python-gotoxy
Cross-platform gotoxy functions.

## Documentation
### gotoxy.py
Code file containing all python functions.

* **GetCursorPosition() (return tuple) (function)**<br>
Returns a tuple with the cursor position. If it cannot be performed, it throws an OSError.

* **SetCursorPosition(x: int, y: int) (function)**<br>
Positions the cursor at the specified x and y coordinates. Only positive integers are accepted as arguments. If it cannot be performed, it throws an OSError.

  In Windows only values from 0 to 32767 are accepted, while in Linux from 0 to 65535.

* **GetTerminalSize() (return tuple) (function)**<br>
Returns the size of the terminal. This function does not contain anything special, it just calls the os.get_terminal_size function. If it cannot be performed, it throws an OSError.

* **SetTerminalSize(columns: int, lines: int) (function)**<br>
Sets the maximum size of the terminal buffer. If it cannot be performed, it throws an OSError.

  In Windows only values from 0 to 32767 are accepted, while in Linux from 0 to 65535.

* **_GetMessageError() (return str) (function)**<br>
Windows exclusive function for obtaining the error messages.

### \_gotoxy.c (Linux only)
Auxiliary code file for Linux.

* **version (const char\*) (constant)**<br>
Constant indicating the code version.

* **GetCursorPosition(int \*code) (return const char\*) (function)**<br>
If there are no problems, it returns a pointer to a raw string containing the cursor position. The position is obtained with the regular expression "\x1b[(\d\*);(\d\*)R".

  The argument that is accepted is to report what happened, If it is 1, there was no problem; if it is 0, an error occurred, and instead of returning the raw string, it returns the error message.

* **SetTerminalSize(ushort columns, ushort lines) (return const char\*) (function)**<br>
Sets the maximum size of the terminal buffer. If it cannot be performed, it throws an OSError.

  If there were no problems the function returns "none", otherwise it returns the error message.

## Notes
* **Compiling \_gotoxy.c to \_gotoxy.so**.<br>
To compile **\_gotoxy.c** type the following in your terminal:
  ```
  gcc -shared -fPIC _gotoxy.c -o _gotoxy.so
  ```
  It must be compiled with a Linux compiler, since there are headers that are not found in Windows.

* **More about \_gotoxy.so**.<br>
**\_gotoxy.so** is only useful on Linux, on Windows it is totally unusable and is not necessary for **gotoxy.py** to work.

* **Folder for import**.<br>
In the **for import** folder you will find **gotoxy.py** and **\_gotoxy.so**, in case you don't want to compile.

## Questions
* **Why only for Linux do you need one more file and why not include the functions directly in Python with ctypes?**<br>
Because in Linux to get the cursor position you need to write an ANSI expression and then read it by manipulating the terminal with some functions (which can be done in Python without any problem), but sometimes you did not get the expected result and when using subprocess (multiprocessing) it was completely useless because it always threw an exception, but these inconveniences do not happen if you do the work in C. The same applies for **SetTerminalSize**.

* **Why does this branch have two more functions and the main branch does not?**<br>
Because the **GetTerminalSize** and **SetTerminalSize** functions do not work as expected.

  **GetTerminalSize** on Linux may tell you that the terminal has 20 height or columns but in reality it is less or more, i.e. it misrepresents the requested information; on Windows it always works fine.

  **SetTerminalSize** in Linux correctly changes the width or rows whenever it can, but it can falsify sizes larger than the terminal can display, when this change is applied it is corrupted so that the characters or words do not break to reach the limit and may overlap on top of others and also, text printouts do not respect the limits set, and in the case of height or columns has no effect, ie nothing happens at all; in Windows if you have a 30x40 terminal you can adjust it to a smaller size, but not bigger, also if the terminal is not maximized it changes size and the biggest inconvenience is that the characters or words are not split or divided when they reach the terminal limit.

  **In the future I may fix it, but it is not currently a priority.**

## Thanks
Thanks to [netzego](https://stackoverflow.com/users/2787738/netzego) for the code to obtain the coordinates in Linux.<br>
[Code in Stack Overflow](https://stackoverflow.com/a/46675451/17948078)
