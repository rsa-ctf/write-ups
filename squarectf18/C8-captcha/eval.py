#!/usr/bin/python
import re
import requests
import base64
import os

ADDSUBMUL = '540'
BRACKET = '340'

size2c = {
    "540" : '-',
    "605" : '8',
    "447" : '1',
    "340" : ')',
    "586" : '3',
    "587" : '4',
    "557" : '2',
    "591" : '9',
    "540" : '*',
    "583" : '5',
    "617" : '0',
    "604" : '6',
    "556" : '7',
    "540" : '+',
    "340" : '(',
}

URL = "https://hidden-island-93990.squarectf.com/ea6c95c6d0ff24545cad"
sess = requests.Session()
resp = sess.get(URL)

base64str = re.findall("base64,(.*?)'", str(resp.content))[0]
evalstr = re.findall("<p>(.*?)</p>", str(resp.content))[0]
token = re.findall(
    '<input type="hidden" name="token" value="(.*?)">', str(resp.content))[0]
print('token', token)

with open('page.html', 'w') as page:
    page.write(resp.content.decode('utf-8'))

with open('font.base64', 'w') as fontttf:
    fontttf.write(base64str)

os.system('base64 -d font.base64 > font.ttf')

os.system('ttx -o font.ttx font.ttf')
ttx = open('font.ttx', 'r').read()

glyphsizes = re.findall('<mtx name="glyph000(.*?)" width="(.*?)" lsb="0"/>', ttx)
g2c = {}

for sizespec in glyphsizes:
    glyphid = sizespec[0]
    glyphsize = sizespec[1]
    if glyphsize == '0':
        continue
    char = None
    # special case for +, -, *. All have size 540.
    if glyphsize == ADDSUBMUL:
        xmax = re.findall(
            '<TTGlyph name="glyph000' + glyphid + '" xMin="0" yMin="0" xMax="(.*?)"', ttx)[0]
        if xmax == '495':
            char = '+'
        elif xmax == '465':
            char = '-'
        elif xmax == '444':
            char = '*'
    # another special case for brackets, they have same size 340
    elif glyphsize == BRACKET:
        # we will deal with this later
        char = '('
    else:
        char = size2c[glyphsize]
    g2c[glyphid] = char

print(g2c)

cmap = re.findall(
    '<map code="(.*?)" name="glyph000(.*?)"/><!-- LATIN (.*?) LETTER (.*?) -->', ttx)
l2c = {}

for i in range(15):
    code = cmap[i][0]
    glyphid = cmap[i][1]
    char = g2c[glyphid]
    capital = cmap[i][2] == 'CAPITAL'
    letter = cmap[i][3] if capital else cmap[i][3].lower()
    if char == '(':
        if letter == evalstr[-1]:
            char = ')'
    l2c[letter] = char

print(l2c)

for key, value in l2c.items():
    evalstr = evalstr.replace(key, value)

print(evalstr)

result = eval(evalstr)

print('result', result)

postresp = sess.post(URL, {'answer': str(result), 'token': token})

flag = 'flag-' + re.findall('flag-([0-9a-zA-Z]+)', str(postresp.content))[0]
print(flag)
