import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("http://localhost:8000/jobs/", timeout=10).text,
                     "html.parser")
rows = [{"title": li.select_one("h2 a").text,
         "city": li.select_one("p.location").text,
         "salary": li.select_one("p.salary").text,
         "posted": li.select_one("p.posted time")["datetime"]}
        for li in soup.select("li.job")]
jobs = pd.DataFrame(rows)

amounts = jobs["salary"].apply(lambda s: [int(x.replace(",", ""))
                                          for x in re.findall(r"[\d,]+", s)])
jobs["salary_min"] = amounts.str[0]
jobs["salary_max"] = amounts.str[1]
jobs["posted"] = pd.to_datetime(jobs["posted"])
jobs["age_days"] = (pd.Timestamp("2027-03-01") - jobs["posted"]).dt.days
print(jobs.sort_values("age_days")
          [["title", "city", "salary_min", "age_days"]].head(3).to_string(index=False))
