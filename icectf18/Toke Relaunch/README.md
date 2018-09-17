# Toke Relaunch - Web
**Author:** - Swathi S Bhat

```
We’ve relaunched our famous website, Toke! Hopefully no one will hack it 
again and take it down like the last time.
```

After a lot of overthinking about the problem, we decided to check `/robots.txt` which gave:
`User-agent: * Disallow: /secret_xhrznylhiubjcdfpzfvejlnth.html`

Navigating to the URL : `https://static.icec.tf/toke/secret_xhrznylhiubjcdfpzfvejlnth.html` gave the flag.

> IceCTF{what_are_these_robots_doing_here}
