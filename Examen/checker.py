import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    if host.endswith("/"):
        host = host[:-1]
    if path.startswith("/"):
        path = path[1:]
    return f"https://{host}/{path}"


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    try:
        r = requests.get(url, timeout=5)
        print("Cod stare:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type"))
    except Exception as e:
        print("Eroare:", e)


def check_site(url):
    try:
        r = requests.get(url, timeout=5)
        srv = r.headers.get("Server")
        if not srv:
            srv = "unknown"
            
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type"),
            "length": len(r.content),
            "server": srv
        }
    except requests.exceptions.Timeout:
        return {"status": None, "error": "timeout"}
    except Exception:
        return {"status": None, "error": "eroare conexiune"}


def scan_sites():
    rezultate = []
    for site in SITES:
        date = check_site(site)
        date["url"] = site
        rezultate.append(date)

    bune = []
    rele = []
    for r in rezultate:
        if r.get("status") == 200:
            bune.append(r)
        else:
            rele.append(r)

    bune.sort(key=lambda x: x["length"], reverse=True)

    for r in bune:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeți")

    print(f"Reușite: {len(bune)} | Eșuate: {len(rele)}")

def check_headers(url):
    try:
        r = requests.get(url, timeout=5)
        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header in r.headers:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100)

        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.exceptions.Timeout:
        return {"status": None, "error": "timeout"}
    except Exception:
        return {"status": None, "error": "site inaccesibil"}