import pandas as pd


def check_books(df, expected_rows=None):
    """Return a list of problems; empty list = all good."""
    problems = []
    if expected_rows and len(df) != expected_rows:
        problems.append(f"{len(df)} rows instead of {expected_rows}")
    for col in ["title", "price"]:
        share = df[col].isna().mean()
        if share > 0.05:
            problems.append(f"{col}: {share:.0%} missing")
    if df["price"].dropna().le(0).any():
        problems.append("prices of 0 or less")
    if df.duplicated(subset="title").any():
        problems.append("duplicate titles")
    return problems


good = pd.DataFrame({"title": ["A", "B", "C"], "price": [5.0, 7.5, 12.0]})
broken = pd.DataFrame({"title": ["A", "B", "B"], "price": [None, None, 0.0]})
print(check_books(good, expected_rows=3))
print(check_books(broken, expected_rows=20))
