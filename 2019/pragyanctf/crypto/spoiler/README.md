
# Spoiler
50 points

**Author**: Kaushik S Kalmady

```
Bran Stark, wants to convey an important information to the Sansa back at winterfell. He sends her a message. The message however, is encrypted though.

Can you find out what Bran is trying to convey??
```

We have `key.pdf` which contains the string `3a2c3a35152538272c2d213e332e3c25383030373a15`. Looks like hex, let's decode it.
```bash
$ xxd -r -p <<<"3a2c3a35152538272c2d213e332e3c25383030373a15"
```

> :,:5%8',-!>3.<%8007:

That doesn't make a lot of sense. But then, like the filename indicates this is probably the key. Where's the ciphertext then?

A little bit of looking around with `hexdump` and `strings` reveals that there are some additional bytes at the end of the pdf after the `EOF` bytes. Let's decode that.

```bash
$ xxd -r -p <<<""0000006a0000006f0000006e000000730000006e0000006f000000770000006900000073000000640000007200000061000000670000006f0000006e00000062000000790000006200000069000000720000007400000068"
```
> jonsnowisdragonbybirth

Well, that's a spoiler. For once I thought this was the flag but then that made no sense. Then I realised that the key we found earlier and the above text both have the same length. That has all the signs of an XOR encryption!

### Solution
```python
import binascii
s = "jonsnowisdragonbybirth"
key = binascii.unhexlify("3a2c3a35152538272c2d213e332e3c25383030373a15")
ans = ""
for i,j in zip(s, key):
    ans += chr(ord(i)^ord(j))
print(ans)
```

## Flag
> PCTF{JON_IS_TARGARYEN}

P.S Not my fault that it's a spoiler.
