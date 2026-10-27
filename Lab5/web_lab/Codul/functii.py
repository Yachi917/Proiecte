import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

print("--- Exercițiul 21 și 23 ---")
def fetch(url: str, timeout: int = 10):
    return requests.get(url, timeout=timeout)

r1 = fetch(BASE_URL)
print("Status implicit:", r1.status_code)
time.sleep(1)
r2 = fetch(BASE_URL, timeout=3)
print("Status timeout=3:", r2.status_code)

print("\n--- Exercițiul 22 și 26 ---")
def get_status(url: str) -> int:
    r = requests.get(url, timeout=TIMEOUT)
    return r.status_code

for cale in ["/", "/robots.txt", "/sitemap.xml"]:
    time.sleep(1)
    print(f"Status pentru {cale}:", get_status(BASE_URL + cale))

time.sleep(1)
try:
    get_status(123)
except requests.exceptions.RequestException as e:
    print("Eroare la get_status(123): Nu este un URL valid")

print("\n--- Exercițiul 24 și 25 ---")
def get_title(html: str) -> str:
    """Returnează textul dintre etichetele <title> dintr-un șir HTML."""
    start = html.find("<title>") + len("<title>")
    stop = html.find("</title>")
    return html[start:stop].strip()

help(get_title)
time.sleep(1)
html_test = fetch(BASE_URL).text
print("Titlul extras:", get_title(html_test))

print("\n--- Exercițiul 27 ---")
def page_exists(url: str) -> bool:
    try:
        r = requests.get(url, timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

time.sleep(1)
print("Există site-ul?", page_exists(BASE_URL))
print("Există site-ul greșit?", page_exists("https://this-domain-does-not-exist.invalid"))

print("\n--- Exercițiul 28 ---")
def check_paths(base: str, paths: list) -> dict:
    rez = {}
    for p in paths:
        time.sleep(1)
        rez[p] = get_status(base + p)
    return rez

print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

print("\n--- Exercițiul 29 ---")
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    r = requests.head(url, timeout=TIMEOUT)
    return r.headers.get(name, default)

time.sleep(1)
print("Header Server:", get_header(BASE_URL, name="Server"))

print("\n--- Exercițiul 30 și 31 ---")
def security_headers(url: str) -> dict:
    r = requests.head(url, timeout=TIMEOUT)
    lista_h = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    rez = {}
    for cap in lista_h:
        rez[cap] = cap in r.headers
    return rez

def score_headers(results: dict) -> str:
    gasite = sum(results.values())
    total = len(results)
    return f"{gasite}/{total}"

time.sleep(1)
sec = security_headers(BASE_URL)
print("Scor securitate:", score_headers(sec))

print("\n--- Exercițiul 32 ---")
def fetch_robots(base: str):
    r = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    if r.status_code == 200:
        return r.text
    return None

def disallowed_paths(robots_text: str) -> list:
    if not robots_text:
        return []
    oprite = []
    linii = robots_text.splitlines()
    for linie in linii:
        if linie.startswith("Disallow:"):
            oprite.append(linie.replace("Disallow:", "").strip())
    return oprite

time.sleep(1)
txt = fetch_robots(BASE_URL)
print("Căi blocate de robots.txt:", disallowed_paths(txt))

print("\n--- Exercițiul 33 ---")
def response_times(*urls) -> dict:
    rez = {}
    for u in urls:
        time.sleep(1)
        t_start = time.perf_counter()
        requests.get(u, timeout=TIMEOUT)
        t_stop = time.perf_counter()
        rez[u] = round(t_stop - t_start, 3)
    return rez

print("Timpi răspuns:", response_times(BASE_URL, ECHO_URL))

print("\n--- Exercițiul 34 ---")
def log(message: str, **details):
    text = message
    for k, v in details.items():
        text += f" | {k}={v}"
    print(text)

log("verificat", url=BASE_URL, status=200)

print("\n--- Verificați-vă ---")
print("print() afișează valoarea pe ecran, dar ea dispare după. return trimite valoarea înapoi în program, ca să o putem folosi mai târziu sau salva într-o variabilă.")