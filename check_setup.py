"""Chapter 0 setup check: run  python check_setup.py

It prints the version of Python and of every package the book uses, then
tests that the Practice Ground site answers. The last line is either
"All set: you are ready for Chapter 1" or the exact problem to fix.
"""
import importlib
import sys
import urllib.request

PACKAGES = [("requests", "requests"), ("beautifulsoup4", "bs4"), ("lxml", "lxml"),
            ("pandas", "pandas"), ("openpyxl", "openpyxl"),
            ("pdfplumber", "pdfplumber"), ("playwright", "playwright"),
            ("selenium", "selenium"), ("scrapy", "scrapy"), ("flask", "flask")]

problems = []
print(f"Python          {sys.version.split()[0]}")
if sys.version_info < (3, 11):
    problems.append("Python is older than 3.11: install the current version (step 0.3).")

for name, module in PACKAGES:
    try:
        importlib.import_module(module)
        from importlib.metadata import version
        print(f"{name:<16}{version(name)}")
    except ImportError:
        print(f"{name:<16}MISSING")
        problems.append(f"{name} is missing: activate .venv, then run "
                        "pip install -r requirements.txt (step 0.6).")

try:
    with urllib.request.urlopen("http://localhost:8000/robots.txt", timeout=5) as r:
        print(f"Practice Ground site: answering (status {r.status})")
except Exception:
    print("Practice Ground site: not answering")
    problems.append("The site is not running: open a second terminal and run "
                    "python run_site.py (step 0.8).")

print()
if problems:
    for p in problems:
        print("PROBLEM:", p)
else:
    print("All set: you are ready for Chapter 1")
