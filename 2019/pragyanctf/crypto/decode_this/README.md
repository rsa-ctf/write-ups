# Decode This
200 points

**Author** : Kaushik S Kalmady

```
Ram has something to show you, which can be of great help. It definitely contains the piece of text "pctf" and whatever follows it is the flag. Can you figure out what it is?

Note: Enclose it in pctf{}
```

This was my favourite challenge from this CTF. We are given a custom encryption function and the ciphertext and our task is to find the plaintext. We are told in the description that the text "pctf" appears in the plaintext and what follows it is the flag.

### Ciphertext
> vuqxyugfyzfjgoccjkxlqvguczymjhpmjkyzoilsxlwtmccclwizqbetwthkkvilkruufwuu

### The Encryption Function
```python
import random

file = open("secret.txt","r")
secret = file.read()

flag = ""
for i in secret:
    if i.isalpha():
        flag += i
l = len(flag)

key = [[int(random.random()*10000) for e in range(2)] for e in range(2)]

i = 0
ciphertext = ""

while i <= (l-2):
    x = ord(flag[i]) - 97
    y = ord(flag[i+1]) - 97
    z = (x*key[0][0] + y*key[0][1])%26 + 97
    w = (x*key[1][0] + y*key[1][1])%26 + 97
    ciphertext = ciphertext + chr(z) + chr(w)
    i = i+2

cipherfile = open('ciphertext.txt','w')
cipherfile.write(ciphertext)
```

There are a few important things to note here.

  - The secret flag only contains alphabets
  - There are 4 elements in the key that we need to find and the bruteforce complexity is `10000^4`
  - Two characters of plaintext give two characters of ciphertext

### The Exploit
We know that `pctf` is in the plaintext - this is extremely key to us reaching the solution. 

Assume that we know where the plaintext `pctf` appears. That means that we know the `x`, `y` from the plaintext as well as the corresponding `z`, `w` from the ciphertext.
Let `x='p', y='c'` give ciphertext `z1, w1` and `x='t', y='f'` give ciphertext `z2, w2`. This now becomes the problem of solving 2 systems of equations with 2 unknowns each with the following parameters.

```
A = [['p','c'], ['t', 'f']]
x1 = [key00, key01], b1 = [z1, z2]
x2 = [key10, key11], b2 = [w1, w2]
```
Note that the equations are `mod 26`. We need to solve the following two systems:
```
A*x1 = b1 mod 26
A*x2 = b2 mod 26
```

Once we obtain `key00, key01, key10, key11` we have the `key` matrix. With this we can then obtain the flag, which as per description follows the text `pctf`. This can again be done by solving a system of equations but the parameters now will be:
```
key = [[key00, key01], [key10, key11]]
x = [x1, x2] (unknown plaintext)
b = [c1, c2] (known ciphertext)
```

We now have to solve the system `A*x = b mod 26` for every pair `(x1, x2)` that appears after the position where `pctf` occurs. 

### Solution
We didn't answer one important thing in the previous section. How do we know where the text `pctf` occurs? 

Truth is we don't. It could be anywhere in the text - so we run the above exploit for every 4 letter set in the text with a sliding window with stride 2. We print the corresponding probable flag assuming that `pctf` occurs at index `i` in the text and check the corresponding output. Since the data is pretty small this doesn't take too long.

I used `Sagemath` to solve the system of equations under mod 26. I'm not aware of any python module that can do this (Sagemath is awesome).

Here is the complete solution script:
```python
#!/usr/bin/env sage -python

import binascii
from sage.all import *

R = IntegerModRing(26)

def solve(inputs, res):
	M = Matrix(R, inputs)
	b = vector(R, res)
	return M.solve_right(b)

def verifyflag(c, key):
	#print "Verifying"
	i = 0
	l = len(c)
	ans = ""
	while i <= (l - 2):
		z = ord(c[i]) - 97
		w = ord(c[i+1]) - 97

		res = [z, w]
		try:
			c1, c2 = solve(key, res)
			ans = ans +  chr(int(c1) + 97) + chr(int(c2)+ 97)
			i += 2

		except:
			print "Couldn't Solve"
			return False

	print ans
	return True

ct = "vuqxyugfyzfjgoccjkxlqvguczymjhpmjkyzoilsxlwtmccclwizqbetwthkkvilkruufwuu"
known = "pctf"

l = len(ct)
i = 0

# Take 4 chars at a time and see if assuming pctf starts there reveals intelligible plaintext after it
while i <= (l - 4):
	print "%d / %d"%(i,l)
	z1 = ord(ct[i]) - 97
	w1 = ord(ct[i+1]) - 97
	z2 = ord(ct[i+2]) - 97
	w2 = ord(ct[i+3]) - 97

	inputs = [[ord('p') - 97, ord('c') - 97], [ord('t') - 97, ord('f') - 97]]
	res1 = [z1, z2]
	res2 = [w1, w2]
	try:
		key00, key01 = solve(inputs, res1)
		key10, key11 = solve(inputs, res2)

		verifyflag(ct[i+4:], [[key00, key01], [key10, key11]])
		i += 2 # Skip two chars : pt, ct are generated in pairs

	except:
		pass

```

Most of the systems won't be solvable and will be skipped. Some of the systems will output some text. The flag is obtained when `i = 38` : `ilikeclimbinghillswhataboutyou`

## Flag
> pctf{ilikeclimbinghillswhataboutyou}

### References
  - [Sagemath](https://www.sagemath.org/index.html)
