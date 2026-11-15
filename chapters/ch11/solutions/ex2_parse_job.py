import requests
from bs4 import BeautifulSoup


def money(text):
    return int(text.strip().replace("£", "").replace(",", ""))


def parse_job_item(li):
    low, high = li.select_one("p.salary").text.split("–")
    return {
        "id": int(li["data-id"]),
        "title": li.select_one("h2.job-title a").text,
        "company": li.select_one("p.company").text,
        "city": li.select_one("p.location").text,
        "salary_min": money(low),
        "salary_max": money(high),
        "posted": li.select_one("p.posted time")["datetime"],
        "new": li.select_one("span.badge") is not None,
    }


html = requests.get("http://localhost:8000/jobs/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
print(parse_job_item(soup.select_one("li.job")))
