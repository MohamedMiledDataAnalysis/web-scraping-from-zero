"""Generate every data file used by the Practice Ground companion website.

All data is synthetic, built from a fixed random seed, so every reader gets
exactly the same site and exactly the outputs printed in the book.
Run:  python site/generate_data.py   (the repository already contains the output)
"""
import json
import random
import string
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

rng = random.Random(2027)

# ---------------------------------------------------------------- library
ADJ = ["Silent", "Golden", "Hidden", "Broken", "Last", "Northern", "Crimson",
       "Quiet", "Distant", "Burning", "Frozen", "Little", "Wild", "Secret",
       "Empty", "Painted", "Lost", "Velvet", "Iron", "Paper", "Midnight",
       "Hollow", "Bright", "Salt", "Glass"]
NOUN = ["Harbour", "Garden", "Letter", "River", "Lantern", "Orchard", "Station",
        "Library", "Island", "Window", "Kingdom", "Bridge", "Compass", "Mirror",
        "Forest", "Clockmaker", "Lighthouse", "Market", "Violin", "Map",
        "Winter", "Kitchen", "Tower", "Meadow", "Archive"]
PATTERNS = ["The {a} {n}", "{a} {n}", "A {n} of {p2}", "The {n} and the {n2}",
            "Beyond the {a} {n}", "{p} in the {n2}", "The {a} {n}: A Novel",
            "Notes from the {n}", "The {n2} of {a} {p}"]


def plural(word):
    return word + "es" if word.endswith(("s", "sh", "ch", "x")) else word + "s"
FIRST = ["Amelia", "Omar", "Clara", "Jonas", "Leila", "Henry", "Sofia", "Tariq",
         "Margot", "Felix", "Nadia", "Oscar", "Ines", "Samuel", "Yara", "Arthur",
         "Elena", "Karim", "Rosa", "Theo", "Maya", "Victor", "Hana", "Louis"]
LAST = ["Whitfield", "Haddad", "Morrow", "Lindqvist", "Okafor", "Brennan",
        "Castell", "Duval", "Fairbairn", "Gallo", "Hartley", "Ibsen", "Kowal",
        "Laurent", "Mendes", "Novak", "Ashby", "Quinlan", "Rahman", "Stroud",
        "Tavares", "Underwood", "Varga", "Winslow"]
CATEGORIES = ["Fiction", "Mystery", "Science Fiction", "Fantasy", "Romance",
              "History", "Biography", "Poetry", "Travel", "Science", "Cookery",
              "Business", "Children", "Philosophy", "Art", "Music", "Sport",
              "Horror", "Humour", "Self Help"]
RATING_WORDS = ["One", "Two", "Three", "Four", "Five"]
OPENINGS = ["A story about {x}.", "An unforgettable journey through {x}.",
            "A careful study of {x}.", "A warm and funny book about {x}.",
            "A dark tale of {x}."]
SUBJECTS = ["family secrets", "a small town by the sea", "lost letters",
            "the first winter after a war", "two rival bakers",
            "an old map and a new friendship", "a city that never sleeps",
            "the quiet courage of ordinary people", "a disappearing island",
            "music, memory and loss"]
CLOSINGS = ["Readers will not put it down.", "Perfect for a long train journey.",
            "The author's finest book so far.", "A favourite of book clubs.",
            "Short chapters make it easy to read."]


def make_title(used):
    while True:
        a, n, n2 = rng.choice(ADJ), rng.choice(NOUN), rng.choice(NOUN)
        if n == n2:
            continue
        t = rng.choice(PATTERNS).format(a=a, n=n, n2=n2, p=plural(n), p2=plural(n2))
        if t not in used:
            used.add(t)
            return t


def slugify(text):
    keep = string.ascii_lowercase + string.digits
    s = "".join(c if c in keep else "-" for c in text.lower())
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


books, used = [], set()
for i in range(1, 1001):
    title = make_title(used)
    stock = rng.choice([0] * 2 + list(range(1, 23)))
    books.append({
        "id": i,
        "title": title,
        "slug": f"{slugify(title)}-{i}",
        "author": f"{rng.choice(FIRST)} {rng.choice(LAST)}",
        "category": rng.choice(CATEGORIES),
        "price": round(rng.uniform(5, 59.99), 2),
        "rating": rng.randint(1, 5),
        "stock": stock,
        "upc": "".join(rng.choice("0123456789abcdef") for _ in range(16)),
        "year": rng.randint(1952, 2026),
        "pages": rng.randint(96, 720),
        "description": " ".join([
            rng.choice(OPENINGS).format(x=rng.choice(SUBJECTS)),
            rng.choice(CLOSINGS)]),
    })
(DATA / "books.json").write_text(json.dumps(books, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- quotes
AUTHORS = {
    "Ada Fernhill": ("1871", "Coldharbour, England", "Ada Fernhill was a schoolteacher who wrote short essays on patience and work."),
    "Tomas Reyna": ("1902", "Valparaiso, Chile", "Tomas Reyna was a sailor and poet who wrote about the sea and friendship."),
    "Mira Okonkwo": ("1948", "Enugu, Nigeria", "Mira Okonkwo is an engineer known for her talks on curiosity and failure."),
    "Henrik Sall": ("1889", "Bergen, Norway", "Henrik Sall was a bookbinder who kept notebooks of everyday sayings."),
    "June Albright": ("1935", "Halifax, Canada", "June Albright was a radio host famous for her morning advice programme."),
    "Rashid Noor": ("1960", "Tunis, Tunisia", "Rashid Noor is a mathematician who writes about learning and mistakes."),
    "Celeste Moreau": ("1912", "Lyon, France", "Celeste Moreau was a chef who wrote about cooking, time and generosity."),
    "Walter Pike": ("1924", "Leeds, England", "Walter Pike was a carpenter and the author of a small book of maxims."),
}
QUOTES = [
    ("Ada Fernhill", "Patience is not waiting; it is working while you wait.", ["patience", "work"]),
    ("Ada Fernhill", "A lesson learned slowly is a lesson kept for life.", ["learning", "patience"]),
    ("Ada Fernhill", "Tidy the desk and the mind will follow.", ["work", "habits"]),
    ("Ada Fernhill", "The pupil who asks twice understands once and for all.", ["learning", "questions"]),
    ("Ada Fernhill", "Small daily efforts build tall houses.", ["work", "habits"]),
    ("Tomas Reyna", "The sea teaches nothing to those who stay on the shore.", ["courage", "sea"]),
    ("Tomas Reyna", "A friend is a harbour you carry with you.", ["friendship", "sea"]),
    ("Tomas Reyna", "Every storm ends in the same calm morning.", ["hope", "sea"]),
    ("Tomas Reyna", "Sail with the wind you have, not the wind you want.", ["courage", "work"]),
    ("Tomas Reyna", "Share your bread and your map.", ["friendship", "generosity"]),
    ("Mira Okonkwo", "Curiosity is the engine; failure is the fuel.", ["curiosity", "failure"]),
    ("Mira Okonkwo", "Break it on purpose, and you will know how it works.", ["curiosity", "learning"]),
    ("Mira Okonkwo", "A failed test is a successful question.", ["failure", "questions"]),
    ("Mira Okonkwo", "Measure twice, ask three times.", ["questions", "work"]),
    ("Mira Okonkwo", "The best tool is the one you understand.", ["work", "learning"]),
    ("Henrik Sall", "A book well bound outlives its binder.", ["work", "time"]),
    ("Henrik Sall", "Kind words cost nothing and are worth a fortune.", ["kindness", "generosity"]),
    ("Henrik Sall", "Read slowly the books you love.", ["reading", "time"]),
    ("Henrik Sall", "The page you skip is the page you needed.", ["reading", "learning"]),
    ("Henrik Sall", "A good habit is a quiet friend.", ["habits", "friendship"]),
    ("June Albright", "Start the day with one good sentence.", ["habits", "hope"]),
    ("June Albright", "Laughter is the shortest road between two people.", ["friendship", "humour"]),
    ("June Albright", "If you cannot be brave, be kind; it often looks the same.", ["courage", "kindness"]),
    ("June Albright", "Morning comes to everyone, even the worried.", ["hope", "time"]),
    ("June Albright", "Listen first; the radio taught me that.", ["questions", "kindness"]),
    ("Rashid Noor", "A mistake you can name is a mistake you can fix.", ["failure", "learning"]),
    ("Rashid Noor", "Understanding is slower than memorising and lasts longer.", ["learning", "time"]),
    ("Rashid Noor", "Every hard problem is three easy problems holding hands.", ["learning", "work"]),
    ("Rashid Noor", "Draw the picture before you write the equation.", ["learning", "habits"]),
    ("Rashid Noor", "The wrong answer shows you where to look.", ["failure", "questions"]),
    ("Celeste Moreau", "Good food takes the time it takes.", ["time", "patience"]),
    ("Celeste Moreau", "Cook for others and you will never eat alone.", ["generosity", "friendship"]),
    ("Celeste Moreau", "Salt, patience and a little butter fix most things.", ["patience", "humour"]),
    ("Celeste Moreau", "Taste as you go, in the kitchen and in life.", ["curiosity", "habits"]),
    ("Celeste Moreau", "A full table is the richest room in the house.", ["generosity", "kindness"]),
    ("Walter Pike", "Measure the wood, not your worries.", ["work", "hope"]),
    ("Walter Pike", "A straight cut starts with a steady breath.", ["patience", "work"]),
    ("Walter Pike", "Sharpen the tool before you blame it.", ["habits", "work"]),
    ("Walter Pike", "Build the chair you would like to sit on.", ["kindness", "work"]),
    ("Walter Pike", "Sawdust on the floor means something was made.", ["work", "humour"]),
]
quotes = [{"id": i + 1, "author": a, "text": t, "tags": tags}
          for i, (a, t, tags) in enumerate(QUOTES)]
authors = [{"name": n, "slug": slugify(n), "born": b, "place": p, "bio": bio}
           for n, (b, p, bio) in AUTHORS.items()]
(DATA / "quotes.json").write_text(json.dumps(quotes, indent=1), encoding="utf-8")
(DATA / "authors.json").write_text(json.dumps(authors, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- shop
P_ADJ = ["Compact", "Smart", "Classic", "Pro", "Eco", "Mini", "Deluxe", "Travel"]
P_NOUN = {"Kitchen": ["Kettle", "Toaster", "Blender", "Coffee Grinder", "Scale"],
          "Office": ["Desk Lamp", "Notebook", "Monitor Stand", "Stapler", "Chair Cushion"],
          "Audio": ["Headphones", "Speaker", "Radio", "Earbuds", "Microphone"],
          "Garden": ["Watering Can", "Pruner", "Bird Feeder", "Hose Reel", "Planter"]}
products, n = [], 0
for cat, nouns in P_NOUN.items():
    for noun in nouns:
        for adj in rng.sample(P_ADJ, 6):
            n += 1
            products.append({
                "id": n, "sku": f"PG-{n:04d}", "name": f"{adj} {noun}",
                "category": cat, "price": round(rng.uniform(4.5, 189), 2),
                "rating": round(rng.uniform(2.5, 5), 1),
                "reviews": rng.randint(0, 900), "in_stock": rng.random() > 0.15})
(DATA / "products.json").write_text(json.dumps(products, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- weather API
STATIONS = [
    {"id": "LON", "name": "London Riverside", "country": "UK", "lat": 51.50, "lon": -0.12},
    {"id": "MAN", "name": "Manchester Hill", "country": "UK", "lat": 53.48, "lon": -2.24},
    {"id": "EDI", "name": "Edinburgh Port", "country": "UK", "lat": 55.95, "lon": -3.19},
    {"id": "PAR", "name": "Paris Canal", "country": "FR", "lat": 48.86, "lon": 2.35},
    {"id": "LYO", "name": "Lyon Confluence", "country": "FR", "lat": 45.76, "lon": 4.83},
]
(DATA / "stations.json").write_text(json.dumps(STATIONS, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- jobs pool
J_TITLES = ["Data Analyst", "Junior Data Engineer", "Python Developer",
            "Business Analyst", "Credit Risk Analyst", "Web Developer",
            "Reporting Analyst", "Data Scientist", "QA Tester",
            "Operations Analyst", "Structured Finance Analyst", "BI Developer"]
J_LEVELS = ["Junior", "Mid-level", "Senior"]
J_CITIES = ["London", "Manchester", "Leeds", "Edinburgh", "Paris", "Lyon",
            "Remote"]
J_COMPANIES = ["Northbridge Bank", "Harbour Analytics", "Meridian Retail",
               "Atlas Tutors", "Kestrel Insurance", "Lumen Health",
               "Riverside Logistics", "Copperfield Energy", "Sable Media"]
J_SKILLS = ["Python", "SQL", "Excel", "Power BI", "R", "AWS", "Git", "Tableau",
            "VBA", "PySpark", "Docker", "Qlik Sense"]
jobs = []
for i in range(1, 401):
    title = rng.choice(J_TITLES)
    level = rng.choice(J_LEVELS)
    base = {"Junior": 30000, "Mid-level": 45000, "Senior": 65000}[level]
    low = base + rng.randint(0, 12) * 1000
    jobs.append({
        "id": 1000 + i, "title": title, "level": level,
        "company": rng.choice(J_COMPANIES), "city": rng.choice(J_CITIES),
        "salary_min": low, "salary_max": low + rng.randint(5, 20) * 1000,
        "skills": sorted(rng.sample(J_SKILLS, 3)),
        # day offset when the job is posted, and how many days it stays online
        "offset": rng.randint(-60, 120), "lifetime": rng.randint(10, 40)})
(DATA / "jobs.json").write_text(json.dumps(jobs, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- price watch
W_ITEMS = ["Wireless Mouse", "Mechanical Keyboard", "27-inch Monitor",
           "USB-C Hub", "Webcam HD", "Laptop Stand", "Noise-Cancelling Headphones",
           "External SSD 1TB", "Smart Watch", "E-reader", "Bluetooth Speaker",
           "Graphics Tablet", "Desk Chair", "Office Printer", "Router Wi-Fi 7",
           "Portable Charger", "Action Camera", "Robot Vacuum", "Air Fryer",
           "Espresso Machine"]
watch = []
for i, name in enumerate(W_ITEMS, 1):
    watch.append({"id": i, "name": name, "base": round(rng.uniform(19, 420), 2),
                  "seed": rng.randint(1, 10**6)})
(DATA / "pricewatch.json").write_text(json.dumps(watch, indent=1), encoding="utf-8")

print(f"books={len(books)} quotes={len(quotes)} products={len(products)} "
      f"jobs={len(jobs)} pricewatch={len(watch)}")
