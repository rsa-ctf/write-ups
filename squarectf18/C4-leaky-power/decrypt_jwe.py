# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-11-10 10:48:40
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-11-10 10:51:48

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