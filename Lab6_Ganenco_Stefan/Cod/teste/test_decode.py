from arsenal.forensics.decode import d, g, x


def test_g():
    assert g("%2Fetc") == "url"
    assert g("48656c6c6f") == "hex"
    assert g("U2FsdXQ=") == "base64"


def test_base64():
    t, b = d("U2FsdXQ=")
    assert t == "base64"
    assert b == b"Salut"


def test_hex():
    t, b = d("54657374")
    assert t == "hex"
    assert b == b"Test"


def test_url():
    t, b = d("%54%65%73%74")
    assert t == "url"
    assert b == b"Test"


def test_xor():
    c = bytes(v ^ 15 for v in b"Test")
    res = x(c)
    assert any(k == 15 and t == "Test" for k, t in res)

 # python -m pytest teste/test_decode.py