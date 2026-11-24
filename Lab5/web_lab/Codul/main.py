import argparse
import csv
from datetime import datetime
from webtools import get_title, fetch, check_paths, site_report, DEFAULT_HEADERS

parser = argparse.ArgumentParser()
parser.add_argument("url")
args = parser.parse_args()

print("--- Exercițiile 44, 45, 47, 48 ---")
print("Folosim antetele:", DEFAULT_HEADERS)
r = fetch(args.url)
print("Titlul extras din modulul webtools:", get_title(r.text))

print("\n--- Exercițiul 49 ---")
rez_paths = check_paths(args.url, ["/", "/robots.txt", "/sitemap.xml"])

with open("report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["path", "status", "checked_at"])
    ora = datetime.now().isoformat()
    for cale, status in rez_paths.items():
        writer.writerow([cale, status, ora])
        
print("Fișierul report.csv a fost generat cu succes.")

print("\n--- Exercițiul 50 ---")
site_report(args.url)

# pentru ca sa ruleze cd web_lab in terminal apoi python main.py https://cybercor.org in terminal.

