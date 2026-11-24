import os
import re
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def b1(p):
    with open(p, "rb") as f:
        c = f.read(8)
    if c.startswith(b"%PDF"):
        return "pdf"
    if c.startswith(b"\x89PNG"):
        return "png"
    if c.startswith(b"\xff\xd8"):
        return "jpeg"
    if c.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return c.hex()


def b2(p):
    with open(p, "rb") as f:
        d = f.read()
    return [m.decode("latin1") for m in re.findall(rb"[ -~]{4,}", d)]


def conv(v, r):
    d = float(v[0]) + float(v[1]) / 60.0 + float(v[2]) / 3600.0
    return -d if r in ("S", "W") else d


def b3(p):
    img = Image.open(p)
    e = img._getexif() or {}
    g = {}
    for k, v in e.items():
        if TAGS.get(k) == "GPSInfo":
            for x, y in v.items():
                g[GPSTAGS.get(x, x)] = y

    if g and "GPSLatitude" in g and "GPSLongitude" in g:
        lat = conv(g["GPSLatitude"], g["GPSLatitudeRef"])
        lon = conv(g["GPSLongitude"], g["GPSLongitudeRef"])
        return lat, lon
    return None


def b4(p, o="gasit.zip"):
    with open(p, "rb") as f:
        d = f.read()
    i = d.find(b"PK\x03\x04")
    if i != -1:
        with open(o, "wb") as f_out:
            f_out.write(d[i:])
        return i
    return -1


if __name__ == "__main__":
    if os.path.exists("probe/foto.jpg"):
        print(b1("probe/foto.jpg"))
        print(b3("probe/foto.jpg"))

    if os.path.exists("probe/ascuns.png"):
        print(b1("probe/ascuns.png"))
        print(b2("probe/ascuns.png")[:5])
        print(b4("probe/ascuns.png"))

 # python forensics.py