# Lost in the Forest - Forensics

**Author:** Kaushik S Kalmady

```
You've rooted a notable hacker's system and you're sure that he has hidden something juicy on there. Can you find his secret?
```

We are given a zip archive `fs.zip` which on extracting gives us a linux directory structure.

I navigate around and the first thing that catches my eye is the file at `/home/hkr/Desktop/clue.png`. It's an image of a fish - but there's nothing fishy about it to be a clue. I reverse search the image and find that it's a Red Herring. That was extremely neat by whoever set this challenge.

Right so that was a dead end.

There were quite a few pictures in the `/home/hkr/Pictures` directory but I didn't bother pursuing it after the last one.

One of the files in `/home/hkr/` named `hzpxbsklqvboyou` seemed to have some form of encoded/encrypted string in it - but still no real lead on how to capture our flag.

`ls -a` reveals that there's a `.bash_history` file in the home folder. This contains all the command that the user has typed on the terminal. I was hopeful of finding some answers here. 

You can go through the contents of the file [here](.bash_history). Upon closer inspection certain lines stand out.

```
wget https://gist.githubusercontent.com/Glitch-is/bc49ee73e5413f3081e5bcf5c1537e78/raw/c1f735f7eb36a20cb46b9841916d73017b5e46a3/eRkjLlksZp

mv eRkjLlksZp tool.py

./tool.py ../secret > ../hzpxbsklqvboyou

shred secret

rm tool.py
```

So the user seemed to have downloaded a file from the internet, rename it to `tool.py`, ran that code on the `secret` file to generate the contents of the `hzpxbsklqvboyou` we found earlier, and then deleted the `secret` and `tool.py`. 

I downloaded the file from the link and examined the code.

```python
#!/usr/bin/python3
import sys
import base64

def encode(filename):
    with open(filename, "r") as f:
        s = f.readline().strip()
        return base64.b64encode((''.join([chr(ord(s[x])+([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] * 3)[x]) for x in range(len(s))])).encode('utf-8')).decode('utf-8')[::-1]*5

if __name__ == "__main__":
    print(encode(sys.argv[1]))
```

This code take a file as input, reads it's contents and encodes it. All we need to do is write a code to reverse the encoding and obtain the flag!

Here's a script to do the decoding.

```python
import base64

with open("hzpxbsklqvboyou", 'r') as f:
	s = f.read()

s = s[:len(s)/5] # Encoded string is replicated 5 times at the end of encoding step
s = s[::-1] # And then string is reversed


# Next base64 decode the string
s = base64.b64decode(s.encode('utf-8'))

# subtract the offsets to achieve reverse of offsetting in the encoding step
s = "".join([chr(ord(s[x])-([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] * 3)[x]) for x in range(len(s))])

print(s)
```

## Flag
> 'IceCTF{good_ol_history_lesson}'
