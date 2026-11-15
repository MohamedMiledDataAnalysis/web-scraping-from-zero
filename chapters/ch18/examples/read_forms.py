import requests
from bs4 import BeautifulSoup

session = requests.Session()
for url in [
    "http://localhost:8000/jobs/",
    "http://localhost:8000/account/login",
]:
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    form = soup.find("form")
    print(url)
    print(
        "  method:",
        form.get("method", "get"),
        "| action:",
        form.get("action", "(this page)"),
    )
    for field in form.find_all(["input", "select"]):
        value = field.get("value", "")
        if field.get("type") == "hidden":
            value = f"<{len(value)} random characters>"
        print(
            "  ",
            field.name,
            field.get("type", ""),
            field.get("name"),
            repr(value),
        )
