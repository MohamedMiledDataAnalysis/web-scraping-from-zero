import json
from pathlib import Path

config = {
    "searches": ["analyst", "python", "data"],
    "cities": ["Leeds", "Manchester", "London", "Remote"],
    "min_salary": 40000,
    "email_to": "me@localhost",
}
Path("output/ch24").mkdir(parents=True, exist_ok=True)
Path("output/ch24/config.json").write_text(json.dumps(config, indent=2))
print(Path("output/ch24/config.json").read_text())
