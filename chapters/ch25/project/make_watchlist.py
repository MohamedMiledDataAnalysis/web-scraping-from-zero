from pathlib import Path

import pandas as pd

watch = pd.DataFrame({
    "id": [3, 7, 9, 14, 19],
    "name": ["27-inch Monitor", "Noise-Cancelling Headphones", "Smart Watch",
             "Office Printer", "Air Fryer"],
    "target": [330.00, 100.00, 316.00, 19.95, 30.50],
})
Path("output/ch25").mkdir(parents=True, exist_ok=True)
watch.to_csv("output/ch25/watchlist.csv", index=False)
print(watch.to_string(index=False))
