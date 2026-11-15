import pandas as pd

print(pd.to_datetime("2027-03-01").date())
print(pd.to_datetime("01/03/2027", format="%d/%m/%Y").date())
print(pd.to_datetime("1 March 2027", format="%d %B %Y").date())
s = pd.Series(["2027-03-01", "2027-02-20", "not a date"])
dates = pd.to_datetime(s, errors="coerce")
print(dates.tolist())
print((pd.Timestamp("2027-03-01") - dates).dt.days.tolist())
