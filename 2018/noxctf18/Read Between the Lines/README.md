# Read Between the Lines - Misc

**Author:** Kaushik S Kalmady

We are given a message.code file. We ascertain the exact nature of the file using the `file` command.

```bash
$ file message.code
message.code: gzip compressed data, was "message", last modified: Fri Jul 20 12:53:57 2018, from Unix
```

As we can see, it's a gzip compressed file. We'll give it the appropriate extension and unzip it.

```bash
$ cp message.code message.code.gz
$ gzip -d message.code.gz
```

It contains an ASCII file named `message` which basically consists of a lot of `+!()[]` symbols.
I was pretty clueless at this point, but one of the teammates suggested that there's a programming language that uses those 6 symbols and we were pointed to [JSFuck](www.jsfuck.com). 

We entered all the text into the IDE and received the output:
> nope

Well, that was that.

Upon closer inspection, we realise that theres a lot of spaces and tabs at the end of the file. Spaces, tabs, newlines. Whitespace!

[Whitespace](https://vii5ard.github.io/whitespace/) is an esoteric programming language written solely using - you guessed it- whitespace. So we entered all the whitespace into an interpreter online and captured the flag!

![flag](whitespace.png)

> The flag is `noxCTF{DaFuckIsWHITESPACE}`
