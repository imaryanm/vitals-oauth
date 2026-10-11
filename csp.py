"""Pins each page's inline <script> and <style> in its Content-Security-Policy by SHA-256, so the
browser runs nothing else. Run it after editing a page: python csp.py"""

import base64
import hashlib
import re
from pathlib import Path

META = re.compile(r'(<meta http-equiv="Content-Security-Policy" content=")[^"]*(")')


def hashes(html, tag):
    found = re.findall(rf"<{tag}>(.*?)</{tag}>", html, re.S)
    digests = [base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() for text in found]
    return " ".join(f"'sha256-{digest}'" for digest in digests) or "'none'"


for page in sorted(Path(__file__).parent.glob("**/index.html")):
    html = page.read_text(encoding="utf-8")
    policy = (
        f"default-src 'none'; script-src {hashes(html, 'script')}; style-src {hashes(html, 'style')}; "
        "base-uri 'none'; form-action 'none'"
    )
    updated, count = META.subn(lambda match: match.group(1) + policy + match.group(2), html)
    if count != 1:
        raise SystemExit(f"{page}: expected one Content-Security-Policy meta tag, found {count}")
    page.write_text(updated, encoding="utf-8", newline="\n")
    print(f"{page.relative_to(Path(__file__).parent)}: {policy}")
