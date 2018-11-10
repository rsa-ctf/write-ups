# C4 : Leaky Power

**Author:** Kaushik S Kalmady


```
C4 is a very advanced AES based defensive system. You are able to monitor the power lines. Is that enough?

You’re given three files:

    powertraces.npy: Measurements (over time) of power consumption of a chip while performing AES encryption
    plaintexts.npy: Corresponding plaintext inputs that were encrypted
    instructions.jwe: File encrypted using the same key as plaintexts.npy.

note: The first two files are NumPy arrays.

note: there's a mistake in the way instructions.jwe was created (the algorithm is A128GCM, not A256GCM).
```

This was a fun and annoying challenge. Fun because there was a lot learnt, annoying because the `instructions.jwe` was not encrypted properly by the organisers. They later uploaded the right file and the challenge was solved.

Firstly, we are given two files which contain the plaintexts that were encrypted and the corresponding powertraces, i.e the power dissipation while encrypting those plaintexts.

I had recently watched a video about **Side Channel Attack using Power Analysis on RSA** by [liveoverflow](https://www.youtube.com/watch?v=bFfyROX7V0s). So it was clear to me that I had to perform the same attack here. There is also another video by liveoverflow on the same attack on AES where he uses the ChipWhisperer to obtain the key (check references below).

The ChipWhisperer [Github Repo](https://github.com/newaetech/chipwhisperer) has example script to break aes using the Power Analysis Side Channel Attack. We will use the modified from of [this script](https://github.com/newaetech/chipwhisperer/blob/develop/software/scripting-examples/break_aes_manual.py) to obtain the flag.

The modified code is in `break_aes_manual_mod.py`.

Running it we obtain the hex encoded 128 bit key: `d2dea057d1145f456796966024a703b2`.

Now we need to use this key to decrypt the encrypted file as per the JSON Web Encryption(JWE) standard. 
The `jwcrypto` module in python can help us do this.

You might want to read a bit about JWE and JWK at https://jwcrypto.readthedocs.io.

First we need to store the key in the JWK readable format. It expects the key to be in base64 encoding and stored as json with some addition information.

```python
>>> import base64
>>> base64.b64encode("d2dea057d1145f456796966024a703b2".decode("hex"))
'0t6gV9EUX0VnlpZgJKcDsg=='
```

As per JWK standards our key object should look like this.

```json
{"k":"0t6gV9EUX0VnlpZgJKcDsg==", "kty":"oct"}
```

We save this in `key.txt`.

The following code performs the decryption.

```python
from jwcrypto import jwk, jwe
import json

with open("key.txt") as f:
    mykey = json.load(f)

key = jwk.JWK(**mykey)

with open("instructions_corrected.jwe") as f:
    enc = f.read()

jwetoken = jwe.JWE()
jwetoken.deserialize(enc)
jwetoken.decrypt(key)
print jwetoken.plaintext
```

Running this we get the corresponding plaintext.

```
CONFIDENTIAL

To disable C4, you will need:
- 6 bits of Dragon Sumac
- 1 nibble of Winter Spice
- 1 byte of Drake Cardamom
- 1 flag with value flag-e2f27bac480a7857de45
- 2 diskfulls of Tundra Chives
- 5 forks

Grind the Dragon Sumac in a cup, making sure you don't break the cup as it's probably a delicate cup. Add a sprinkle of
liquid ice to turn it into a cream-like paste, then add the Winter Spice, first almost everything, then the last tiny
remnants.

Fill a pan with elemental water, add the mixture and cool it down with how cool you are, then bring the mixture
to a boil. Let it cool down to the body temperature of a reptile before adding the Drake Cardamom and Tundra Chives,
all at once of one, then half at a time of the other.

Bring everything back to a boil, turn of the heat, mix with the forks and let everything cool down. If you
touch the liquid and it burns you, it hasn't cooled down enough.

Whisk the mixture heavily to aerate it. Stop when it's frothy.

Drinking the potion will disable C4.

note: A small, but very cold amount is needed for the potion to be effective. Mixing it in a milkshake could work, but
be wary of brain freeze.

```

## Flag
> flag-e2f27bac480a7857de45

## References
  - Breaking AES with ChipWhisperer: https://www.youtube.com/watch?v=FktI4qSjzaE
  - RSA Power Analysis Side Channel Attack: https://www.youtube.com/watch?v=bFfyROX7V0s
