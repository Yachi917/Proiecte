import argparse
import base64
import hashlib
import json
import re
from urllib.parse import unquote


def f(b):
    return len(b) > 0 and all(32 <= x <= 126 or x in (10, 13, 9) for x in b)


def g(s):
    s = s.strip()
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"


def d(s):
    t = g(s)
    try:
        if t == "base64":
            return t, base64.b64decode(s)
        if t == "hex":
            return t, bytes.fromhex(s)
        if t == "url":
            return t, unquote(s).encode()
    except Exception:
        pass
    return "necunoscut", s.encode()


def r(s, n=8):
    h = []
    c = s.strip()
    for _ in range(n):
        t, b = d(c)
        if t == "necunoscut":
            break
        h.append(t)
        try:
            c = b.decode()
        except Exception:
            c = b.decode("latin1")
        if f(b) and g(c) == "necunoscut":
            break
    return h, c


def x(b):
    res = []
    for k in range(256):
        c = bytes(v ^ k for v in b)
        if f(c):
            try:
                res.append((k, c.decode()))
            except Exception:
                res.append((k, c.decode("latin1")))
    return res


def h(t, w):
    t = t.strip().lower()
    m = {32: hashlib.md5, 40: hashlib.sha1, 64: hashlib.sha256}.get(len(t))
    if not m:
        return None
    with open(w, encoding="latin1") as f_in:
        for line in f_in:
            c = line.strip()
            if m(c.encode()).hexdigest() == t:
                return c
    return None


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("i")
    p.add_argument("--fisier", action="store_true")
    p.add_argument("--xor", action="store_true")
    p.add_argument("--hash", action="store_true")
    p.add_argument("--wordlist", default="probe/wordlist.txt")
    a = p.parse_args()

    s = ""
    b = b""
    if a.fisier:
        with open(a.i, "rb") as fp:
            b = fp.read()
        try:
            s = b.decode()
        except Exception:
            s = ""
    else:
        s = a.i
        b = a.i.encode()

    out = {}

    if a.xor:
        res = x(b)
        out = {"mod": "xor", "gasite": [{"k": k, "t": t} for k, t in res]}
        for k, t in res:
            print(k, t)
    elif a.hash:
        ans = h(s or b.decode(), a.wordlist)
        out = {"mod": "hash", "gasit": ans}
        print(ans)
    else:
        steps, res = r(s)
        out = {"mod": "straturi", "straturi": steps, "rezultat": res}
        print(steps, res)

    with open("arsenal/forensics/fisa.json", "w") as fp:
        json.dump(out, fp, indent=2)

# cd Lab6
# python arsenal/forensics/decode.py (Get-Content probe/mesaj.txt)
# python arsenal/forensics/decode.py probe/xor.bin --fisier --xor
# python arsenal/forensics/decode.py (Get-Content probe/hashuri.txt -TotalCount 1) --hash --wordlist probe/wordlist.txt

