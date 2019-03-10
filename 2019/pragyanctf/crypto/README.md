
# Help Rabin
150 points

**Author** : Kaushik S Kalmady

We are given a public key file(`publickey.pem`), encryption code(`encrypt.py`) and the ciphertext. It's clear from the title that this involves the Rabin Cryptosystem.

Let's take a look at the encryption script first.
```python
from Crypto.Util.number import *
import random

def nextPrime(prim):
    if isPrime(prim):
        return prim
    else:
        return nextPrime(prim+1)

p = getPrime(512)
q = nextPrime(p+1)
while p%4 != 3 or q%4 !=3:
    p = getPrime(512)
    q = nextPrime(p+1)

n = p*q
m = open('secret.txt').read()
m = bytes_to_long(m)

m = m**e
c = (m*m)%n
c = long_to_bytes(c)
c = c.encode('hex')

cipherfile = open('ciphertext.txt','w')
cipherfile.write(c)
```

We'll go step by step.

### Prime Generation
There are a few things to note here. Two primes are generated. `p` is a random 512 bit prime, and if we notice `q` is the next prime after `p`, i.e. `p` and `q` are consecutive primes. There should be a few sirens flaring up in the background at this moment - but we'll hold them off for now.

Next, we compute `n = p * q` and this is used as the modulus.

### Encryption
It's not clear from the encryption code that this is indeed Rabin Cryptosystem. This is because essential Rabin encryption is same as RSA with e=2. So ideally we need to have `c = m^2 mod n`, but here what we have is `m^(2*e) mod n`. We dont know what `n` and `e` are yet, and for this to be the Rabin cryptosystem, `e` has to be equal to 1 here so that we have `c = m^2 mod n`.

### The Public Key
We are given a pem file containing the public key which is essentially just contains a base64 string. I used openssl's rsa commands to read it  - however this was an arbitrary choice. My guess was that since we needed to know both `e` and `n` the public key could be in rsa form itself.
```bash
$ openssl rsa -noout -text -inform PEM -in publickey.pem -pubin
```
```
Public-Key: (1023 bit)
Modulus:
    61:5b:e0:98:72:7a:e6:10:de:9c:10:48:19:f3:a1:
    f7:cc:5b:31:44:81:0b:38:d4:f4:d5:1b:be:11:d9:
    ca:20:f2:87:ee:d0:23:6b:ce:d1:fe:44:3a:33:5a:
    2f:33:c7:a8:ac:68:f0:9f:c5:f3:8b:fe:37:4a:92:
    07:d3:07:3d:40:2c:7a:65:a3:0b:60:f7:5b:10:e4:
    3a:29:67:30:aa:22:d3:25:27:f7:20:3e:c9:be:cc:
    6a:7a:0d:d7:0a:5c:e3:d1:d5:f2:a8:db:98:68:e8:
    a4:53:4e:ef:70:5f:2c:6a:83:26:c8:8a:53:6b:82:
    7c:88:bc:00:05:22:7a:c9
Exponent: 1 (0x1)
```

And turns out what I expected was right. The value of `e` is indeed 1, confirming that this is the rabin cryptosystem. The value of n upon converting to decimal is `68367741643352408657735068643514841659753216083862769094847066695306696933618090026602354837201210914348646470450259642887798188510482019698636160200778870456236361521880907328722252080005877088416283896813311117096542977573101128888124000494645965045855288082328139311932783360168599377647677632122110245577`.

### The Exploit
Right so we have everything in place. We know the ciphertext, the encryption algo and the public key. So the next obvious step is to figure out how to obtain the private key so that we can decrypt the ciphertext.

Let's bring the sirens to the forefront now. I metioned earlier that it was a terrible thing to have `p` and `q` to be consecutive primes. This is because, since `n = p * q` and p and q are close to each other we can actualy approximate `p ~ sqrt(n)`. From here on we can do a linear search for the exact value of p (it should be somewhere close to `sqrt(n))` and there we have it, n is factorised. 

This is important because now we can decrypt the ciphertext with the knowledge of `p` and `q`. The Wikipedia article from Rabin Cryptoystem contains the algorithm for decryption when `p` and `q` are known. I just had to implement it and we get the flag.

### Solution
```
import gmpy2
from Crypto.Util.number import *

#openssl rsa -noout -text -inform PEM -in publickey.pem -pubin
n = 68367741643352408657735068643514841659753216083862769094847066695306696933618090026602354837201210914348646470450259642887798188510482019698636160200778870456236361521880907328722252080005877088416283896813311117096542977573101128888124000494645965045855288082328139311932783360168599377647677632122110245577
sq,b = gmpy2.iroot(n,2)
while n%sq != 0:
    sq += 1
p = sq
q = n / sq

with open("ciphertext.txt") as f:
    ct = f.read()
ct = ct.decode('hex')
ct = bytes_to_long(ct)

q = int(q)
p = int(p)
assert(p * q == n)

mp = pow(ct, (p+1)/4, p)
mq = pow(ct, (q+1)/4, q)

from rsasim.gcd_utils import xgcd
g, yp, yq = xgcd(p, q)

r = (yp*p*mq + yq*q*mp) % n
mr = n - r
s = (yp*p*mq - yq*q*mp) % n
ms = n - s
for num in [r,mr,s,ms]:
    print(long_to_bytes(num))
```

## Flag
> pctf{R4b1n_1s_th3_cut3st}

### References
  - [Rabin Cryptosystem](https://en.wikipedia.org/wiki/Rabin_cryptosystem)
  - [rsasim](https://github.com/kaushiksk/rsasim)
