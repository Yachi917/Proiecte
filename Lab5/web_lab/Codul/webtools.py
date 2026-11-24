import requests
import time
import urllib.parse
import re
import socket
import ssl
from datetime import datetime
import json

TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Student"}

def fetch(url: str, timeout: int = TIMEOUT):
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url: str) -> int:
    r = fetch(url)
    return r.status_code

def get_title(html: str) -> str:
    start = html.find("<title>") + len("<title>")
    stop = html.find("</title>")
    return html[start:stop].strip()

def security_headers(url: str) -> dict:
    r = requests.head(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
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
    return f"{gasite}/{len(results)}"

def extract_links(html: str) -> list:
    gasite = re.findall(r'href="([^"]+)"', html)
    return list(set(gasite))

def split_links(links: list, domain: str) -> tuple:
    interne, externe = [], []
    d_baza = urllib.parse.urlparse(domain).netloc
    for lnk in links:
        complet = urllib.parse.urljoin(domain, lnk)
        d_lnk = urllib.parse.urlparse(complet).netloc
        if d_lnk == d_baza:
            interne.append(complet)
        else:
            externe.append(complet)
    return interne, externe

def check_paths(base: str, paths: list) -> dict:
    rez = {}
    for p in paths:
        time.sleep(1)
        rez[p] = get_status(urllib.parse.urljoin(base, p))
    return rez

def fetch_robots(base: str):
    r = fetch(urllib.parse.urljoin(base, "/robots.txt"))
    if r.status_code == 200:
        return r.text
    return None

def disallowed_paths(robots_text: str) -> list:
    if not robots_text:
        return []
    oprite = []
    for linie in robots_text.splitlines():
        if linie.startswith("Disallow:"):
            oprite.append(linie.replace("Disallow:", "").strip())
    return oprite

def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)

def cert_days_left(hostname: str) -> int:
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
            cert = ssl_sock.getpeercert()
            zile = ssl.cert_time_to_seconds(cert['notAfter'])
            data_exp = datetime.fromtimestamp(zile)
            return (data_exp - datetime.now()).days

def site_report(url: str):
    r = fetch(url)
    titlu = get_title(r.text)
    dom = urllib.parse.urlparse(url).netloc
    
    ip = resolve(dom)
    
    time.sleep(1)
    r_http = requests.get(f"http://{dom}", headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    redir = []
    for ist in r_http.history:
        redir.append(f"{ist.status_code} -> {ist.url}")
    redir_str = ", ".join(redir) if redir else "Nicio redirecționare"
    
    time.sleep(1)
    scor_sec = score_headers(security_headers(url))
    
    zile_cert = cert_days_left(dom)
    
    toate_lnk = extract_links(r.text)
    int_lnk, ext_lnk = split_links(toate_lnk, url)
    
    time.sleep(1)
    txt_rob = fetch_robots(url)
    cai_oprite = disallowed_paths(txt_rob)
    
    date_raport = {
        "url": url,
        "status": r.status_code,
        "titlu": titlu,
        "ip": ip,
        "redirects": redir,
        "scor_securitate": scor_sec,
        "zile_certificat": zile_cert,
        "legaturi_interne": len(int_lnk),
        "legaturi_externe": len(ext_lnk),
        "cai_interzise": cai_oprite
    }
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(date_raport, f, indent=2)
        
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {r.status_code}")
    print(f"Titlu:             {titlu}")
    print(f"Adresă IP:         {ip}")
    print(f"Redirecționări:    {redir_str}")
    print(f"Scor securitate:   {scor_sec}")
    print(f"Certificat:        {zile_cert} de zile rămase")
    print(f"Legături:          {len(int_lnk)} interne, {len(ext_lnk)} externe")
    print(f"Căi interzise:     {', '.join(cai_oprite) if cai_oprite else 'Niciuna'}")
    print("Salvat în report.json")

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))