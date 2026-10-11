# vitals-oauth

A static page on GitHub Pages that hands a Withings sign-in back to a private [Vitals](https://github.com/imaryanm/vitals-django) server.

After you sign in, Withings only sends the browser back to a public `https` address (no IP addresses, no ports other than 443, checked when the Withings app is saved). The Vitals server is only reachable on the home network and over Tailscale. So the Withings app's callback URL is this page:

```
https://imaryanm.github.io/vitals-oauth/withings/
```

It forwards the browser, with Withings' `code` and `state`, to `/withings/callback/` on the Vitals address the sign-in started from.

## Why it's safe

- **Nothing to steal here.** The page holds no data, secrets or server addresses. The address to return to rides in the OAuth `state`, which the Vitals server made and checks against the session that started the sign-in.
- **The code is useless on its own.** It expires in 30 seconds, works once, and only turns into access together with the Withings app's client secret, which never leaves the Vitals server.
- **Not an open redirect.** It only forwards to private addresses (10.x, 172.16-31.x, 192.168.x, 127.x, Tailscale's 100.64-127.x, `localhost` and `*.ts.net` names), and only to the path `/withings/callback/`.
- **Nothing else runs.** No third-party scripts, styles or fonts. A Content Security Policy allows only the page's own inline script and style, pinned by their SHA-256, and `no-referrer` keeps the URL from being passed on.
- **The server stays private.** Nothing on the Vitals server is exposed to the internet; once connected, it talks to Withings directly over https.

The page is only needed while connecting; GitHub Pages can be switched off in between.

## Changing a page

The Content Security Policy pins each inline script and style by hash. After editing a page, run:

```
python csp.py
```
