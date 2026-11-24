import requests
import urllib.request
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

print("--- Exercițiul 1 ---")
print("Versiune requests:", requests.__version__)

time.sleep(1)

print("\n--- Exercițiul 2 ---")
r1 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (requests.get):", r1.status_code)

time.sleep(1)

from requests import get
r2 = get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (get):", r2.status_code)

time.sleep(1)

print("\n--- Exercițiul 3 ---")
import requests as rq
r3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (rq.get):", r3.status_code)

time.sleep(1)

print("\n--- Exercițiul 4 ---")
cerere = urllib.request.Request(BASE_URL, headers={'User-Agent': 'WebLab-Student'})
with urllib.request.urlopen(cerere, timeout=TIMEOUT) as r4:
    print("Cod de stare (urllib):", r4.status)
    date = r4.read()
    text = date.decode("utf-8")
    print("Primele 200 de caractere:\n", text[:200])

time.sleep(1)

print("\n--- Exercițiul 5 ---")
print(dir(requests))

print("\n--- Exercițiul 6 ---")
r6 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cerere reușită folosind parametrul timeout:", r6.status_code)

time.sleep(1)

print("\n--- Exercițiul 7 ---")
t_start = time.perf_counter()
r7 = requests.get(BASE_URL, timeout=TIMEOUT)
t_stop = time.perf_counter()

t1 = t_stop - t_start
t2 = r7.elapsed.total_seconds()

print(f"Timp perf_counter: {t1:.4f}s")
print(f"Timp response.elapsed: {t2:.4f}s")

print("\n--- Exercițiul 8 ---")
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")