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
print(p * q == n)

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