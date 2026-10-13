import checker


def main():
    print("--- Partea 1 ---")
    print("Partea 1, build_url fara slash:", checker.build_url("example.com", "login"))
    print("Partea 1, build_url cu slash:  ", checker.build_url("example.com", "/login"))
    print("Partea 1, is_https (https):    ", checker.is_https("https://example.com"))
    print("Partea 1, is_https (http):     ", checker.is_https("http://example.com"))

    print("\n--- Partea 2 ---")
    print("Test URL valid:")
    checker.show_response("https://example.com")
    print("\nTest URL inexistent (eroare):")
    checker.show_response("http://this-site-does-not-exist.invalid")

    print("\n--- Partea 3 ---")
    site1 = "https://example.com"
    site2 = "http://this-site-does-not-exist.invalid"
    site3 = "https://httpbin.org/status/404"
    print("Partea 3, check_site (ok):        ", checker.check_site(site1))
    print("Partea 3, check_site (inexistent):", checker.check_site(site2))
    print("Partea 3, check_site (404):       ", checker.check_site(site3))

    print("\n--- Partea 4 ---")
    checker.scan_sites()

    print("\n--- Partea 5 ---")
    url_ok = "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"
    url_simplu = "https://example.com"
    url_gresit = "http://this-site-does-not-exist.invalid"

    print("Partea 5, check_headers (anteturi prezente):", checker.check_headers(url_ok))
    print("Partea 5, check_headers (anteturi lipsa):   ", checker.check_headers(url_simplu))
    print("Partea 5, check_headers (site inaccesibil): ", checker.check_headers(url_gresit))


if __name__ == "__main__":
    main()