# Garfeld - Crypto
**Author:** - Swathi S Bhat
 
```
You found the marketing campaign for a brand new sitcom. Garfeld! It has a secret message engraved on it. 
Do you think you can figure out what they're trying to say?
```

![garfeld](garfeld.png)


Using the number on the top right and omitting { and _ characters in the string, applying a simple shift against each character 
yielded the flag. 

```python
s = 'IjgJUOPLOUVAIRUSGYQUTOLTDSKRFBTWNKCFT'
n = '07271978'
q = len(s)/len(n)
n = (n*(q+1))[:len(s)]
print n
print s

flag=""
for (i,j) in zip(s,n):
    if i.isupper():
        flag+=chr( int(ord(i)-int(j)-65)%26 + 65)
    else:
        flag+=chr( int(ord(i)-int(j)-97)%26 +97)
print flag

```
Running the above code gave:
> IceCTFIDONTTHINKGRONSFELDLIKESMONDAYS

Adding the _ and { characters, the flag turned out to be: `IceCTF{I_DONT_THINK_GRONSFELD_LIKES_MONDAYS}`
