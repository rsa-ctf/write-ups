# Decryptor - Crypto
**Author:** Kaushik S Kalmady

```
I created this nice decryptor for RSA ciphertexts, you should try it out!

nc chal.noxale.com 4242

Oh, and someone told me to give this to you: 
N = 140165355674296399459239442258630641339281917770736077969396713192714338090714726890918178888723629353043167144351074222216025145349467583141291274172356560132771690830020353668100494447956043734613525952945037667879068512918232837185005693504551982611886445611514773529698595162274883360353962852882911457919 

c = 86445915530920147553767348020686132564453377048106098831426077547738998373682256014690928256854752252580894971618956714013602556152722531577337080534714463052378206442086672725486411296963581166836329721403101091377505869510101752378162287172126836920825099014089297075416142603776647872962582390687281063434 

e = 65537
```

We have a server that decrypts the ciphertext we give it. Obviously, it wont decrypt the ciphertext `c` that we are supposed to decrypt to solve the challenge. So we need a workaround.

We have to basically decrypt `c` without asking the server to specifically do so. We have the RSA public key `(e,N)` to encrypt any plaintext we wish to decrypt.

This requires a RSA Blinding Attack. I have a detailed notebook walkthrough on the topic [here](https://gist.github.com/kaushiksk/57a74e7160ee0b8d3bfce1c80bbfb134).

We first choose a random integer, say `x` and encrypt it.
```python
>>> x = 1234
>>> xenc = pow(x, e, N) # RSA encryption is just modular exponentiation
>>> payload = (xenc * c) % N # # we ask the server to decrypt xenc * c (We are blinding the server to the actual ciphertext)
>>> hex(payload) # This is what we will give the server (It only takes hex input and gives hex output)
'0x36244f275b346c7b2ce5c04461cb4fb8bc8555b4d34d3c05e05a46ddd1866ffa05ce80b465661bb35d24852fb5134497a68298bc4714bb7f88b4d5b68fc46c637cce29b9f9c822c36d2872f92c49223adab141bc1e89cab07789b6f4bfe97b4fc35975683ec711d310de884106e7e6d191e38cee91fc07ef2ded80305006ff42L'
```

We send the hex string to the server (without the `0x` and the `L` at the end and receive the decrypted hex string)
>  2145551b48c3bbdcf95054a6466ce8e15ba628a

Now to get the plaintext corresponding to c, we need to multiply the returned number with x^-1 (x inverse modulo N).

It's simple math. Assuming the private key at the server is `d`
```
payload = (x^e * c) mod N
returned_value = (x^e * c)^d mod N

Hence,
returned_value = (x^(ed) * c^d) mod N
	       = (x * c^d) mod N, since x^(ed) = x mod N
```

Now if we multiply x^-1 to the returned value, we will be left with c^d which is nothing but the plaintext we need.
I use the inverse function from [here](https://github.com/kaushiksk/rsasim/blob/master/rsasim/gcd_utils.py).

```python
>>> ans = int('2145551b48c3bbdcf95054a6466ce8e15ba628a', 16)
>>> xinv = rsasim.gcd_utils.inverse(x, N)
>>> (ans * xinv) % N
9620282652174541515632189048064332019229821L
```

We just need to convert this number to a string and we should have our flag.

```python
def num_to_str(num):
   res = ""
   while num > 0:
       res = chr(num % 256) + res
       num = num / 256
   return res
```

We feed the number to our handy function and capture the flag!
```python
>>> num_to_str(9620282652174541515632189048064332019229821L)
'noxCTF{0u7sm4r73d}'
```

