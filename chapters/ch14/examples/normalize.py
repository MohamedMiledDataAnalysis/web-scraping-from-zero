import pandas as pd

answer = {
    "results": [
        {
            "id": 1,
            "name": "Pro Kettle",
            "price": {"amount": 39.5, "currency": "GBP"},
            "tags": ["kitchen"],
        },
        {
            "id": 2,
            "name": "Mini Radio",
            "price": {"amount": 24.0, "currency": "GBP"},
            "tags": ["audio", "travel"],
        },
    ]
}
print(pd.DataFrame(answer["results"]).to_string())
flat = pd.json_normalize(answer["results"])
print(flat.to_string())
print(flat.explode("tags")[["name", "tags"]].to_string())
