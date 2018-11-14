# C9: postfuscator

**Author:** Kaushik S Kalmady

```
The humans who designed C9 were afraid that the Charvises would disavow their pact.

The humans therefore decided to build an additional defense system, C9, using an ancient programming language. A programming language that Charvises didn’t even know is a programming language!

Can you figure out the correct input?

postfuscator.jar
```

We are given a bash file that takes input from the user and generates a postscript file. If the input is such that the provided conditions are met, we get the flag. In fact if we look at the code it is clear that the flag is nothing but the substring `${key:2:20}` which is bash for 20 characters from index 2 in key, where key here is the input we provide.

So we need to now understand the postscript code that is given and tailor our input accordingly.

So going through the code and understanding it took some effort. I found this [postscript reference](https://atrey.karlin.mff.cuni.cz/~milanek/PostScript/Reference/) quite useful. 

The first part is fairly clear, the input we provide is prepended with a `'%'` and then an XOR operation is performed with `4L0ksa1t` as the XOR key. This key is repeated multiple times till it fits the input length.

Next there is a hardcoded string in the file. It is hex decoded, lzw decoded and then the obtained string in stored in a variable `buf`. I tried looking up decryptors for LZW but this didn't really help me make any progress. Then the slack channel of the CTF had someone comment about debugging postscript. 

I installed ghostscript which is a postscript interpreter. Next I added some debug lines to print the value of `buf`.

```
 (buf = ) print
 buf 118 string cvs print
 (\n) print
```

This is present in the ![postfuscator-modified.sh](postfuscator-modified.sh) file. Running this script with any arbitrary input should now prints the buffer contents. 

Now examining the code further and checking the values of `i` and `c` it was clear that our initial interpretation of the input being xored was indeed right. 

These are the overall operations translated into understandable format
```python
encrypt_string = xor('%' + input, "4L0ksa1t")
if(encrypt_string == buf):
    test_str = True
else test_str = False

if test_str:
    print flag
```

Here, we know `buf` and the XOR key. Now our aim is to obtain `input` so that `encrypt_str` will be equal to `buf` and we'll have the flag!

The solution script goes like this:

```python
# Target buffer, got this by debugging ps file using GhostScript
buf = '1712009367807218646859018292134521568805686127287089876612468382748236461208592688982686121828975882178245515674851882'

# Allowed chars are a-f0-9
poss =  range(97,103) + range(48, 58)

# What are the possible values you can get by xor-ing char c
# with all values in poss
def run(c, poss):
    return [(i, ord(c)^i) for i in poss]

def decrypt(buf, ans, poss):
    salt = "4L0ksa1t"
    i = 1 # First char is %
    while len(buf) > 0:
        vals = run(salt[i % len(salt)], poss)
        i = i + 1
        bestval = None

        # Choose the value which gives the longest length prefix in buf when xored
        # This is important because we are only allowed 65 chars in input that we
        # supply. There can be multiple inputs that give target on xor, but we need
        # the one that fits in 65 chars
        for val in vals:
         if buf.find(str(val[1]))==0:
             if bestval is None or len(str(val[1])) > len(str(bestval[1])):
                 bestval = val

        ans = ans + chr(bestval[0])
        buf = buf[len(str(bestval[1])):]
        # print bestval 
    return ans

ans = '%' # We know this is first char and ord('%') ^ ord('4') = 17

ans = decrypt(buf[2:], ans, poss) # First two chars is buf are 17 which is ord('%') ^ ord('4')
assert len(ans) == 65

print "Input: "+ans
print 'flag-'+ans[3:23]

```

> Input: 406016abbe1ac8a7a2d7140232c58f68bc9932424e778c025b2893efa5d0edff

## Flag
> flag-6016abbe1ac8a7a2d714
