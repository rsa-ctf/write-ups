# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-11-14 23:53:11
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-11-15 00:04:07

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

ans = decrypt(buf[2:], ans, poss)
assert len(ans) == 65

print "Input: "+ans
print 'flag-'+ans[3:23]
