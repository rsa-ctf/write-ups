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
		i += 2

	except:
		pass
	


