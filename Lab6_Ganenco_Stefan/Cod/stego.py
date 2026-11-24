from PIL import Image


def h(p_in, p_out, m):
    im = Image.open(p_in).convert("RGB")
    px = list(im.getdata())
    bits = "".join(f"{x:08b}" for x in (m + b"\x00"))

    res = []
    i = 0
    n = len(bits)

    for r, g, b in px:
        c = [r, g, b]
        for j in range(3):
            if i < n:
                c[j] = (c[j] & ~1) | int(bits[i])
                i += 1
        res.append(tuple(c))

    out = Image.new("RGB", im.size)
    out.putdata(res)
    out.save(p_out)


def e(p):
    im = Image.open(p).convert("RGB")
    px = list(im.getdata())
    bits = ""
    res = bytearray()

    for r, g, b in px:
        for v in (r, g, b):
            bits += str(v & 1)
            if len(bits) == 8:
                b_val = int(bits, 2)
                if b_val == 0:
                    return bytes(res)
                res.append(b_val)
                bits = ""
    return bytes(res)


if __name__ == "__main__":
    h("probe/foto.jpg", "stego.png", b"FLAG{ascuns_in_pixeli}")
    print(e("stego.png").decode())

 # python stego.py

