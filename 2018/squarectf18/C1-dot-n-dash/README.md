# C1: dots-n-dashes

**Author:** Hrishikesh Hiraskar

```
The instructions to disable C1 were considered restricted. As a result, they were stored only in encoded form.

The code to decode the instructions was regrettably lost due to cosmic radiation. However, the encoder survived.

Can you still decode the instructions to disable C1? 
```

We are given a html file and a `instructions.txt` which is full of dot-n-dash.

On opening the html file, there is a interface which provides and text box with encode and decode buttons. A quick encode of sample text gives us string of dots-n-dashes. Hmmm, the `instructions.txt` is the encoded file which we have to decode.

But the decode button just erases all the text. After opening the source of html file it is clear that there are two functions `_encode` and `_decode` of which `_encode` did something but `_decode` just returned empty string. That's why it erased everything. Our task is to complete this `_decode` function.

To do that, we should know what `_encode` did. The function is divided into three parts, let's see what each part did.

## Part 1

```javascript
var a=[];
for (var i=0; i<input.length; i++) {
    var t = input.charCodeAt(i);
    for (var j=0; j<8; j++) {
        if ((t >> j) & 1) {
            a.push(1 + j + (input.length - 1 - i) * 8);
        }
    }
}
```

It is iterating through each character, and for each character, it is computing set bits in ascii representation and pushing the reverse index of the set bits.

For example, if the character is `A` which is `0x41 = 0100 0001`, the set bits are `a = [1, 7]`. Remember the _reverse index_.

## Part 2

```javascript
var b = [];
while (a.length) {
    var t = (Math.random() * a.length)|0;
    b.push(a[t]);
    a = a.slice(0, t).concat(a.slice(t+1));
}
```

It is running a while loop while `a` has positive length. At each iteration, it is calculating a random number in range of `a`s length, pushing it to `b`, then removing that element from `a`.

Javascript has fancy way of removing an element from list :D. Qouting [Juice WRLD](https://www.youtube.com/watch?v=LGNsVA2C9EM)

> I cannot change you so I must replace you (OH)

## Part 3

```javascript
var r = '';
while (b.length) {
    var t = b.pop();
    r = r + "-".repeat(t) + ".";
}
return r;
```

This is running over `b`, and for each element in `b`, appending element times dash and a dot to a string and then returning the string. This is our encoded string. 

It is now clear that the encoder is calculating the set bits indexes and converting each set bit index to dashes delimited by dot. Now, we can just reverse these steps to get the decoded text.

Following steps show process to decode the text:

1. Get set bits indexes from the encoded text.
2. Convert set bits list to a binary string with bits set accordingly.
3. Convert the binary string to ascii text.

Only thing we need to take care is that the indexing order. The set bits are reverse index.

The following snippet shows the full `_decode` function:

```javascript
function _decode(input) {
  var dashes = input.split(".");
  console.log("dashes", dashes);

  var setBits = [];
  var maxSetBit = 0;
  for (var i=0; i<dashes.length-1; i++) {
    setBits.push(dashes[i].length);
    maxSetBit = Math.max(maxSetBit, setBits[i]);
  }
  console.log("setBits", setBits);
  console.log("maxSetBit", maxSetBit);

  var len = Math.floor(maxSetBit/8) + ((maxSetBit%8 > 0) ? 1 : 0);
  console.log("len", len);

  var binaryString = "0".repeat(len*8);
  for (var i=0; i<setBits.length; i++)
    binaryString = binaryString.replaceAt(setBits[i]-1, '1');
  binaryString = binaryString.split("").reverse().join("");
  console.log("binaryString", binaryString);
  
  var string = '';
  for (var i=0; i<len; i++) {
    var binaryChar = binaryString.slice(i*8, (i+1)*8);
    var charCode = parseInt(binaryChar, 2);
    string += String.fromCharCode(charCode);
  }
  
  return string;
}
```

We also need to calculate the length of the string, which can be easily calculated from max index in set bits. Also, I had to create a function to replace char at index in string. The full code can be found in this folder.

Decoding the `instructions.txt` gave following:

```
Instructions to disable C1:
1. Open the control panel in building INM035.
2. Hit the off switch.

Congrats, you solved C1! The flag is flag-bd38908e375c643d03c6.
```

And we have our f14444g!!!