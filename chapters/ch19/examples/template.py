import pandas as pd

path = "output/ch19/files/cover_pool_synthetic.xlsx"
raw = pd.read_excel(path, header=None)
print(raw.to_string())

issuer = raw.iloc[1, 1]
date = raw.iloc[2, 1]
fields = pd.read_excel(path, header=4)
values = dict(zip(fields["Field"], fields["Value"]))
pool, bonds = values["M.1.1"], values["M.1.2"]
print(issuer, date)
print(f"Overcollateralisation: {(pool / bonds - 1) * 100:.1f}%")
print("WA LTV:", values["M.2.2"], "| loans:", values["M.2.1"])
