# Reference - Web
**Author:**  Swathi S Bhat

```
What is your reference again?

http://chal.noxale.com:5000
```

The challenge provides a link to a site that upon visiting displayed:
> where the **** did you come from?

Since the challenge was titled Reference, we figured out it must be something to do with the referer header.
Now the task was to find out what to set the referer to. This was easy as `index.js` directly gave it away. 
![index.js](/indexJS.png)

Using Python's `requests` module, we set the referer to `http://google.com`.
```python
>>> import requests
>>> url='http://chal.noxale.com:5000/check_from_google'
>>> headers={'referer':'http://google.com'}
>>> r=requests.get(url,headers=headers)
>>> r.text
u'bm94Q1RGe0cwb2dMM18xc180bFc0WXNfVXJfYjNTVF9SM2YzcjNuYzN9\n'
```

Upon base64 decoding the text, we get the flag.
> noxCTF{G0ogL3_1s_4lW4Ys_Ur_b3ST_R3f3r3nc3}
