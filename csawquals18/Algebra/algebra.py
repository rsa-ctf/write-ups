from pwn import *
from sympy.core import sympify
from sympy import solve
rem = remote("misc.chal.csaw.io", 9002)


s = rem.recv()
print(s)

def getx(eqn):
    sympy_eq = sympify("Eq(" + eqn.replace("=", ",") + ")")
    ans = solve(sympy_eq)
    print(ans)
    if ans == True: # Input was invalid
        return "0"
    return str(round(ans[0], 2))
#
while True:
    s = rem.recvline()
    print(s)
    rem.recv()
    ans = getx(s)
    print(ans)
    rem.sendline(ans)
    s = rem.recvline()
    print(s)
