#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>

const char *version = "0.2";

const char *GetCursorPosition(int *code){
    /*If there are no problems, it returns a pointer to a raw string containing the cursor position.
    The position is obtained with the regular expression "\x1b[(\d*);(\d*)R".

    The argument that is accepted is to report what happened.*/
    struct termios save, raw;

    tcgetattr(0, &save);
    cfmakeraw(&raw);
    tcsetattr(0, TCSANOW, &raw);

    if (isatty(fileno(stdin))){
        write(1, "\x1B[6n", 5);

        char c;
        char *dinamyc_string = NULL;
        int count = 0;

        while (1){
            read(0, &c, 1);

            if (count == 0){
                dinamyc_string = malloc(2);
            } else{
                dinamyc_string = realloc(dinamyc_string, count+2);
            }

            dinamyc_string[count] = c;

            if (c == 'R'){
                break;
            }

            count++;
        }

        tcsetattr(0, TCSANOW, &save);
        *code = 1;
        return dinamyc_string;    
    }

    *code = 0;
    tcsetattr(0, TCSANOW, &save);

    char *out = malloc(255);
    sprintf(out, "[Errno %i] %s", errno, strerror(errno));

    return out;
}

const char *SetTerminalSize(ushort columns, ushort lines){
    //Sets the cursor position.
    struct winsize size = {lines, columns, 0, 0};
    if (ioctl(fileno(stdout), TIOCSWINSZ, &size) != -1){
        return "none";
    }

    char *out = malloc(255);
    sprintf(out, "[Errno %i] %s", errno, strerror(errno));

    return out;
}
