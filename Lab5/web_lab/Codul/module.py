import requests
import time
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

print("--- Exercițiul 35 ---")
u_parse = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("Scheme:", u_parse.scheme)
print("Netloc:", u_parse.netloc)
print("Path:", u_parse.path)
print("Query:", u_parse.query)
print("Fragment:", u_parse.fragment)

print("\n--- Exercițiul 36 ---")
print(urllib.parse.urljoin(BASE_URL, "/about"))
print(urllib.parse.urljoin(BASE_URL, "contact.html"))
print(urllib.parse.urljoin(BASE_URL, "../index.html"))

print("\n--- Exercițiul 37 ---")
def extract_links(html: str) -> list:
    gasite = re.findall(r'href="([^"]+)"', html)
    fara_dubluri = list(set(gasite))
    return fara_dubluri

r = requests.get(BASE_URL, timeout=TIMEOUT)
toate_linkurile = extract_links(r.text)
print("S-au găsit", len(toate_linkurile), "legături unice.")

print("\n--- Exercițiul 38 ---")
def split_links(links: list, domain: str) -> tuple:
    interne = []
    externe = []
    for lnk in links:
        complet = urllib.parse.urljoin(domain, lnk)
        domeniu_lnk = urllib.parse.urlparse(complet).netloc
        domeniu_baza = urllib.parse.urlparse(domain).netloc
        if domeniu_lnk == domeniu_baza:
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe

int_lnk, ext_lnk = split_links(toate_linkurile, BASE_URL)
print(f"Interne: {len(int_lnk)}, Externe: {len(ext_lnk)}")

print("\n--- Exercițiul 39 ---")
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

f_test = ImageFinder()
f_test.feed(test_html)
print("Test:", f_test.images)

assert f_test.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

time.sleep(1)
r_img = requests.get(BASE_URL, timeout=TIMEOUT)
f_real = ImageFinder()
f_real.feed(r_img.text)
print(len(f_real.images), "imagini găsite pe site")
for img in f_real.images:
    print(img)

print("\n--- Exercițiul 40 ---")
def page_fingerprint(url: str) -> str:
    r = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(r.content).hexdigest()

time.sleep(1)
h1 = page_fingerprint(BASE_URL)
time.sleep(1)
h2 = page_fingerprint(BASE_URL)
print("Hash 1:", h1)
print("Hash 2:", h2)

print("\n--- Exercițiul 41 ---")
time.sleep(1)
r_h = requests.get(BASE_URL, timeout=TIMEOUT)

with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(r_h.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    date_h = json.load(f)
    print("Content-Type din fișier:", date_h.get("Content-Type"))

print("\n--- Exercițiul 42 ---")
def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)

dom = urllib.parse.urlparse(BASE_URL).netloc
print("Adresa IP pentru", dom, "este:", resolve(dom))

print("\n--- Exercițiul 43 ---")
def cert_days_left(hostname: str) -> int:
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
            cert = ssl_sock.getpeercert()
            zile = ssl.cert_time_to_seconds(cert['notAfter'])
            data_exp = datetime.fromtimestamp(zile)
            zile_ramase = (data_exp - datetime.now()).days
            return zile_ramase

print("Zile până expiră certificatul:", cert_days_left(dom))
