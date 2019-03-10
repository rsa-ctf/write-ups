# Algebra - Misc
**Author**: Kaushik S Kalmady

We are given a server that throws algebra equations at us. You could try solving it by hand, but you'll realise soon that's not tractable. The equations keep getting more complex. We need to automate this.

We use Sympy. It's a python module that provides handy algebraic and mathematical computation capabilities. This [stackoverflow post](https://stackoverflow.com/questions/50043189/solve-equation-string-with-python-to-every-symbol) has a good answer on how to solve an equation represented as a string. 

All we need to do is couple this code with the code to communicate with the server and we can see how sympy solves the equations thrown by the server one by one. Until it fails to parse one particular equation. I tried to see if there was something wrong with what I was doing but it seemed like the equation itself might be imbalanced. I just capture this particular case and return 0 for it. Turns out it's the last equation and we get the flag.

Here's the entire code.

```python
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

while True:
    s = rem.recvline()
    print(s)
    rem.recv()
    ans = getx(s)
    print(ans)
    rem.sendline(ans)
    s = rem.recvline()
    print(s)

```

## Flag
> flag{y0u_s0_60od_aT_tH3_qU1cK_M4tH5}
