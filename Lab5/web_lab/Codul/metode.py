import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

print("--- Exercițiul 9 ---")
r = requests.get(BASE_URL, timeout=TIMEOUT)
print("Status:", r.status_code)
print("OK:", r.ok)
print("URL:", r.url)
print("Encoding:", r.encoding)

print("\n--- Exercițiul 10 ---")
r.raise_for_status()

time.sleep(1)
try:
    r_gresit = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    print("Codul returnat de server pentru pagina inexistentă este:", r_gresit.status_code)
    r_gresit.raise_for_status()
except requests.HTTPError:
    print("Pagina nu există! Serverul a returnat o eroare HTTP.")

print("\n--- Exercițiul 11 ---")
for nume, val in r.headers.items():
    print(f"{nume}: {val}")

print("\n--- Exercițiul 12 ---")
print("Server:", r.headers.get("Server", "lipsește"))
print("Content-Type:", r.headers.get("Content-Type", "lipsește"))
print("content-type:", r.headers.get("content-type", "lipsește"))

print("\n--- Exercițiul 13 ---")
nr_cyber = r.text.lower().count("cyber")
print("Cyber apare de:", nr_cyber)

print("\n--- Exercițiul 14 ---")
html = r.text
start = html.find("<title>") + len("<title>")
stop = html.find("</title>")
titlu = html[start:stop].strip()
print("Titlul extras:", titlu)

print("\n--- Exercițiul 15 ---")
linii = html.splitlines()
print("Total linii:", len(linii))
linia_max = max(linii, key=len)
print("Lungimea celei mai lungi linii:", len(linia_max))

print("\n--- Exercițiul 16 ---")
if r.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

print("\n--- Exercițiul 17 ---")
time.sleep(1)
r_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
for ist in r_http.history:
    print(ist.status_code, ist.url)
print("URL final:", r_http.url)

print("\n--- Exercițiul 18 ---")
time.sleep(1)
r_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
r_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("Lungime HEAD:", len(r_head.content))
print("Lungime GET:", len(r_get.content))

print("\n--- Exercițiul 19 ---")
if r.cookies:
    for c in r.cookies:
        print(c.name, c.secure)
else:
    print("Niciun cookie setat")

print("\n--- Exercițiul 20 ---")
s = requests.Session()
s.headers.update({"User-Agent": "WebLab-Student"})

time.sleep(1)
r_sess = s.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Raspuns session:", r_sess.text)