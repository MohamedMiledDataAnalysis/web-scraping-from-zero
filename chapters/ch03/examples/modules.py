import time
from datetime import date
from pathlib import Path

start = time.perf_counter()
time.sleep(0.5)                       # wait half a second
print(round(time.perf_counter() - start, 1), "seconds")

print(date(2027, 3, 1).isoformat())

folder = Path("output") / "ch03"
folder.mkdir(parents=True, exist_ok=True)
file = folder / "notes.txt"
file.write_text("Scraped on 2027-03-01\n", encoding="utf-8")
print(file.read_text(encoding="utf-8"), end="")
print(file.exists(), file.name, file.suffix)
