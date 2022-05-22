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

* **\_GetMessageError() (return str) (function)**<br>
Windows exclusive function for obtaining the error messages.

### \_gotoxy.c (Linux only)
Auxiliary code file for Linux.

* **version (const char\*) (constant)**<br>
Constant indicating the code version.

* **GetCursorPosition(int \*code) (return const char\*) (function)**<br>
If there are no problems, it returns a pointer to a raw string containing the cursor position. The position is obtained with the regular expression "\x1b[(\d\*);(\d\*)R".

  The argument that is accepted is to report what happened, If it is 1, there was no problem; if it is 0, an error occurred, and instead of returning the raw string, it returns the error message.

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
Because in Linux to get the cursor position you need to write an ANSI expression and then read it by manipulating the terminal with some functions (which can be done in Python without any problem), but sometimes you did not get the expected result and when using subprocess (multiprocessing) it was completely useless because it always threw an exception, but these inconveniences do not happen if you do the work in C.

* **Why does this branch need two more functions?**<br>
Go to **"Why does this branch have two more functions and the main branch does not?"** in the questions section that is in the ["with_terminal_size"](https://github.com/FrankC64/Python-gotoxy/tree/with_terminal_size) branch to find out the answer.

## Thanks
Thanks to [netzego](https://stackoverflow.com/users/2787738/netzego) for the code to obtain the coordinates in Linux.<br>
[Code in Stack Overflow](https://stackoverflow.com/a/46675451/17948078)
