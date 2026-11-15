import shutil
from pathlib import Path

import pandas as pd

folder = Path("output/ch19/pools")
folder.mkdir(parents=True, exist_ok=True)
source = Path("output/ch19/files/cover_pool_synthetic.xlsx")
for name in ["pool_a.xlsx", "pool_b.xlsx", "pool_c.xlsx"]:
    shutil.copy(source, folder / name)


def read_cover_pool(path):
    raw = pd.read_excel(path, header=None)
    fields = pd.read_excel(path, header=4)
    record = {
        "file": Path(path).name,
        "issuer": raw.iloc[1, 1],
        "date": raw.iloc[2, 1],
    }
    record.update(dict(zip(fields["Field"], fields["Value"])))
    return record


pools = pd.DataFrame(
    [read_cover_pool(p) for p in sorted(folder.glob("*.xlsx"))]
)
print(
    pools[["file", "issuer", "M.1.1", "M.2.2"]].to_string(index=False)
)
