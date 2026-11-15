import pandas as pd

df = pd.DataFrame({
    "url": ["/b/1", "/b/2", "/b/1", "/b/3"],
    "price": [26.93, 19.20, 26.93, 6.56],
    "scraped": ["09:00", "09:00", "09:05", "09:05"],
})
print(df.duplicated().sum(), "identical rows")
print(df.duplicated(subset="url").sum(), "repeated urls")
print(df.drop_duplicates(subset="url", keep="last").to_string(index=False))
