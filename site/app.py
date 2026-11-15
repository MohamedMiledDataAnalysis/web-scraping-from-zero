"""Practice Ground — the companion website of "I Finally Understand Web Scraping".

Start it from the repository folder with:   python run_site.py
Then open http://localhost:8000 in your browser.

Every page is built from the files in site/data, so the site never changes
and every reader sees exactly what the book prints.
"""
import datetime as dt
import hashlib
import json
import math
import secrets
import time
from collections import defaultdict, deque
from functools import wraps
from pathlib import Path

from flask import (Flask, Response, abort, jsonify, redirect, render_template,
                   request, send_from_directory, session, url_for)

HERE = Path(__file__).parent
DATA = HERE / "data"
FILES = HERE / "files"

BOOK_DATE = dt.date(2027, 3, 1)          # the date used in every book output
PER_PAGE_BOOKS = 20
PER_PAGE_QUOTES = 10
PER_PAGE_JOBS = 15
API_KEYS = {"pg-demo-2027": "Book reader"}
API_LIMIT, API_WINDOW = 10, 10            # 10 requests per 10 seconds
TROUBLE_LIMIT, TROUBLE_WINDOW = 5, 10      # /trouble/limited: 5 per 10 seconds

app = Flask(__name__)
app.secret_key = "practice-ground-not-a-real-secret"
app.config["SITE_DATE"] = None             # None = BOOK_DATE; "live" = today


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


BOOKS = load("books.json")
BOOK_BY_SLUG = {b["slug"]: b for b in BOOKS}
QUOTES = load("quotes.json")
AUTHORS = {a["name"]: a for a in load("authors.json")}
AUTHOR_BY_SLUG = {a["slug"]: a for a in AUTHORS.values()}
PRODUCTS = load("products.json")
STATIONS = {s["id"]: s for s in load("stations.json")}
JOBS = load("jobs.json")
WATCH = load("pricewatch.json")
RATING_WORDS = ["One", "Two", "Three", "Four", "Five"]


def cat_slug(name):
    return name.lower().replace(" ", "-")


CATEGORY_BY_SLUG = {cat_slug(b["category"]): b["category"] for b in BOOKS}


# ------------------------------------------------------------------ helpers
def site_today():
    """The site's 'today'. ?day=YYYY-MM-DD lets you visit the site on another day."""
    day = request.args.get("day")
    if day:
        try:
            return dt.date.fromisoformat(day)
        except ValueError:
            abort(400, "day must look like 2027-03-01")
    if app.config["SITE_DATE"] == "live":
        return dt.date.today()
    return app.config["SITE_DATE"] or BOOK_DATE


def stable_unit(*parts):
    """A number between 0 and 1 that is always the same for the same inputs."""
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return int(h[:12], 16) / 16**12


def paginate(items, page, per_page):
    pages = max(1, math.ceil(len(items) / per_page))
    if page < 1 or page > pages:
        abort(404)
    start = (page - 1) * per_page
    return items[start:start + per_page], pages


class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.hits = defaultdict(deque)

    def check(self, key):
        """Return (allowed, remaining, retry_after_seconds)."""
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] >= self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False, 0, max(1, math.ceil(self.window - (now - q[0])))
        q.append(now)
        return True, self.limit - len(q), 0


api_limiter = RateLimiter(API_LIMIT, API_WINDOW)
trouble_limiter = RateLimiter(TROUBLE_LIMIT, TROUBLE_WINDOW)
flaky_counter = {"n": 0}


@app.context_processor
def inject():
    return {"site_today": site_today, "rating_words": RATING_WORDS}


# ------------------------------------------------------------------ home
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/robots.txt")
def robots():
    text = ("# Practice Ground robots.txt\n"
            "User-agent: *\n"
            "Disallow: /private/\n"
            "Disallow: /admin/\n"
            "Crawl-delay: 1\n"
            "\n"
            "User-agent: BadBot\n"
            "Disallow: /\n"
            "\n"
            "Sitemap: http://localhost:8000/sitemap.xml\n")
    return Response(text, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    urls = ["/", "/library/", "/quotes/", "/tables/", "/api/", "/shop/",
            "/files/", "/jobs/", "/prices/", "/terms/"]
    body = "".join(f"<url><loc>http://localhost:8000{u}</loc></url>" for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f"{body}</urlset>")
    return Response(xml, mimetype="application/xml")


@app.route("/terms/")
def terms():
    return render_template("terms.html")


@app.route("/private/")
def private():
    return render_template("simple.html", title="Private area",
                           text="robots.txt asks robots not to visit this page.")


# ------------------------------------------------------------------ library
@app.route("/library/")
@app.route("/library/page-<int:page>.html")
def library(page=1):
    books, pages = paginate(BOOKS, page, PER_PAGE_BOOKS)
    cats = sorted(CATEGORY_BY_SLUG.items(), key=lambda kv: kv[1])
    return render_template("library_list.html", books=books, page=page,
                           pages=pages, total=len(BOOKS), cats=cats,
                           heading="All books", base="/library/")


@app.route("/library/category/<slug>/")
@app.route("/library/category/<slug>/page-<int:page>.html")
def library_category(slug, page=1):
    if slug not in CATEGORY_BY_SLUG:
        abort(404)
    name = CATEGORY_BY_SLUG[slug]
    items = [b for b in BOOKS if b["category"] == name]
    books, pages = paginate(items, page, PER_PAGE_BOOKS)
    cats = sorted(CATEGORY_BY_SLUG.items(), key=lambda kv: kv[1])
    return render_template("library_list.html", books=books, page=page,
                           pages=pages, total=len(items), cats=cats,
                           heading=name, base=f"/library/category/{slug}/")


@app.route("/library/book/<slug>.html")
def library_book(slug):
    book = BOOK_BY_SLUG.get(slug) or abort(404)
    ld = {
        "@context": "https://schema.org", "@type": "Book",
        "name": book["title"], "author": {"@type": "Person", "name": book["author"]},
        "genre": book["category"], "numberOfPages": book["pages"],
        "datePublished": str(book["year"]), "isbn": None, "sku": book["upc"],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": book["rating"],
                            "bestRating": 5},
        "offers": {"@type": "Offer", "price": f'{book["price"]:.2f}',
                   "priceCurrency": "GBP",
                   "availability": "https://schema.org/InStock" if book["stock"]
                   else "https://schema.org/OutOfStock"},
    }
    del ld["isbn"]
    return render_template("library_book.html", book=book,
                           cat=cat_slug(book["category"]),
                           ld=json.dumps(ld, indent=2))


# ------------------------------------------------------------------ quotes
def quote_page(items, page, base, heading):
    shown, pages = paginate(items, page, PER_PAGE_QUOTES)
    tags = sorted({t for q in QUOTES for t in q["tags"]})
    return render_template("quotes.html", quotes=shown, page=page, pages=pages,
                           base=base, heading=heading, tags=tags,
                           authors=AUTHORS)


@app.route("/quotes/")
@app.route("/quotes/page/<int:page>/")
def quotes(page=1):
    return quote_page(QUOTES, page, "/quotes/", "Quotes to scrape")


@app.route("/quotes/tag/<tag>/")
@app.route("/quotes/tag/<tag>/page/<int:page>/")
def quotes_tag(tag, page=1):
    items = [q for q in QUOTES if tag in q["tags"]]
    if not items:
        abort(404)
    return quote_page(items, page, f"/quotes/tag/{tag}/", f"Quotes tagged “{tag}”")


@app.route("/quotes/author/<slug>/")
def quotes_author(slug):
    author = AUTHOR_BY_SLUG.get(slug) or abort(404)
    items = [q for q in QUOTES if q["author"] == author["name"]]
    return render_template("author.html", author=author, quotes=items)


@app.route("/quotes/js/")
@app.route("/quotes/js/page/<int:page>/")
def quotes_js(page=1):
    shown, pages = paginate(QUOTES, page, PER_PAGE_QUOTES)
    return render_template("quotes_js.html", data=json.dumps(shown), page=page,
                           pages=pages)


# ------------------------------------------------------------------ tables
@app.route("/tables/")
def tables():
    return render_template("tables.html")


# ------------------------------------------------------------------ open API
def api_error(status, message):
    resp = jsonify({"error": message, "status": status})
    resp.status_code = status
    return resp


def require_key(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key") or request.args.get("api_key")
        if not key:
            return api_error(401, "Missing API key. Send it in the X-API-Key header.")
        if key not in API_KEYS:
            return api_error(403, "This API key is not valid.")
        ok, remaining, retry = api_limiter.check(key)
        if not ok:
            resp = api_error(429, "Too many requests. Wait and try again.")
            resp.headers["Retry-After"] = str(retry)
            resp.headers["X-RateLimit-Remaining"] = "0"
            return resp
        resp = view(*args, **kwargs)
        resp.headers["X-RateLimit-Limit"] = str(API_LIMIT)
        resp.headers["X-RateLimit-Remaining"] = str(remaining)
        return resp
    return wrapper


def observation(station, day):
    s = STATIONS[station]
    doy = day.timetuple().tm_yday
    seasonal = 7 * math.cos(2 * math.pi * (doy - 200) / 365)
    base = 28 - 0.33 * s["lat"]
    temp = base + seasonal + (stable_unit(station, day, "t") - 0.5) * 6
    rain_chance = stable_unit(station, day, "r")
    rain = 0.0 if rain_chance < 0.55 else round((rain_chance - 0.55) * 30, 1)
    return {"station": station, "date": day.isoformat(),
            "temp_max_c": round(temp + 3.5, 1), "temp_min_c": round(temp - 3.5, 1),
            "rain_mm": rain}


@app.route("/api/")
def api_docs():
    return render_template("api.html", key=next(iter(API_KEYS)))


@app.route("/api/v1/stations")
@require_key
def api_stations():
    country = request.args.get("country")
    items = [s for s in STATIONS.values() if not country or s["country"] == country]
    return jsonify({"count": len(items), "stations": items})


@app.route("/api/v1/observations")
@require_key
def api_observations():
    station = request.args.get("station", "")
    if station not in STATIONS:
        return api_error(400, "Unknown station. See /api/v1/stations.")
    try:
        start = dt.date.fromisoformat(request.args.get("start", "2027-01-01"))
        end = dt.date.fromisoformat(request.args.get("end", "2027-01-31"))
        page = int(request.args.get("page", 1))
    except ValueError:
        return api_error(400, "Dates must look like 2027-01-31 and page must be a number.")
    if end < start or (end - start).days > 366:
        return api_error(400, "end must be after start, at most 366 days later.")
    days = [start + dt.timedelta(d) for d in range((end - start).days + 1)]
    size = 10
    pages = max(1, math.ceil(len(days) / size))
    if page < 1 or page > pages:
        return api_error(400, f"page must be between 1 and {pages}.")
    chunk = days[(page - 1) * size: page * size]
    nxt = None
    if page < pages:
        nxt = url_for("api_observations", station=station, start=start.isoformat(),
                      end=end.isoformat(), page=page + 1)
    return jsonify({"station": station, "page": page, "pages": pages,
                    "count": len(days), "next": nxt,
                    "results": [observation(station, d) for d in chunk]})


# ------------------------------------------------------------------ shop (JavaScript)
@app.route("/shop/")
def shop():
    cats = sorted({p["category"] for p in PRODUCTS})
    return render_template("shop.html", cats=cats)


@app.route("/shop/api/products")
def shop_products():
    time.sleep(0.4)  # a real API takes a moment to answer
    cat = request.args.get("category")
    sort = request.args.get("sort", "id")
    items = [p for p in PRODUCTS if not cat or p["category"] == cat]
    if sort == "price":
        items = sorted(items, key=lambda p: p["price"])
    elif sort == "rating":
        items = sorted(items, key=lambda p: -p["rating"])
    try:
        page = int(request.args.get("page", 1))
        per = min(int(request.args.get("per_page", 12)), 50)
    except ValueError:
        return api_error(400, "page and per_page must be numbers")
    pages = max(1, math.ceil(len(items) / per))
    chunk = items[(page - 1) * per: page * per] if 1 <= page <= pages else []
    return jsonify({"page": page, "pages": pages, "total": len(items),
                    "products": chunk})


@app.route("/shop/api/product/<int:pid>")
def shop_product_api(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return jsonify(p)
    return api_error(404, "No product with this id")


@app.route("/shop/product/<int:pid>")
def shop_product(pid):
    if not any(p["id"] == pid for p in PRODUCTS):
        abort(404)
    return render_template("shop_product.html", pid=pid)


# ------------------------------------------------------------------ account (login)
USERS = {"reader": "practice"}


def orders_for(user):
    out = []
    for i in range(1, 13):
        b = BOOKS[(i * 37) % len(BOOKS)]
        d = BOOK_DATE - dt.timedelta(days=i * 9)
        out.append({"number": f"PG-{20270 + i}", "date": d.isoformat(),
                    "item": b["title"], "total": b["price"],
                    "status": "Delivered" if i > 2 else "On its way"})
    return out


def login_required(view):
    @wraps(view)
    def wrapper(*a, **k):
        if "user" not in session:
            return redirect(url_for("login", next=request.path))
        return view(*a, **k)
    return wrapper


@app.route("/account/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not token or token != session.get("csrf_token"):
            error = "Security token missing or wrong. Load the login page first."
        elif USERS.get(request.form.get("username")) != request.form.get("password"):
            error = "Wrong username or password."
        else:
            session["user"] = request.form["username"]
            return redirect(request.args.get("next") or url_for("account"))
    session["csrf_token"] = secrets.token_hex(16)
    return render_template("login.html", token=session["csrf_token"], error=error), \
        (400 if error else 200)


@app.route("/account/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/account/")
@login_required
def account():
    return render_template("account.html", user=session["user"],
                           orders=orders_for(session["user"]))


@app.route("/account/orders.csv")
@login_required
def account_csv():
    rows = ["number,date,item,total,status"]
    for o in orders_for(session["user"]):
        item = '"' + o["item"].replace('"', '""') + '"'
        rows.append(f'{o["number"]},{o["date"]},{item},{o["total"]:.2f},{o["status"]}')
    return Response("\n".join(rows) + "\n", mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=orders.csv"})


# ------------------------------------------------------------------ files
@app.route("/files/")
def files():
    listing = []
    for p in sorted(FILES.iterdir()):
        if p.is_file():
            listing.append({"name": p.name, "size": p.stat().st_size})
    return render_template("files.html", files=listing)


@app.route("/files/<path:name>")
def file_download(name):
    return send_from_directory(FILES, name, as_attachment=True)


# ------------------------------------------------------------------ trouble zone
@app.route("/trouble/")
def trouble():
    return render_template("trouble.html")


@app.route("/trouble/status/<int:code>")
def trouble_status(code):
    if code < 200 or code > 599:
        abort(400)
    if code in (301, 302, 303, 307, 308):
        return redirect(url_for("trouble_moved"), code=code)
    return Response(f"<html><body><h1>Status {code}</h1></body></html>",
                    status=code, mimetype="text/html")


@app.route("/trouble/moved")
def trouble_moved():
    return render_template("simple.html", title="You were redirected",
                           text="This page has moved here permanently.")


@app.route("/trouble/old-page")
def trouble_old():
    return redirect(url_for("trouble_moved"), code=301)


@app.route("/trouble/slow")
def trouble_slow():
    seconds = min(float(request.args.get("seconds", 3)), 30)
    time.sleep(seconds)
    return render_template("simple.html", title="Slow page",
                           text=f"This page took {seconds:g} seconds to answer.")


@app.route("/trouble/limited")
def trouble_limited():
    ok, remaining, retry = trouble_limiter.check(request.remote_addr)
    if not ok:
        return Response("Too many requests", status=429,
                        headers={"Retry-After": str(retry)})
    return Response(f"OK - {remaining} requests left in this window",
                    mimetype="text/plain")


@app.route("/trouble/flaky")
def trouble_flaky():
    flaky_counter["n"] += 1
    if flaky_counter["n"] % 3 != 0:      # fails twice, then works once
        return Response("Service temporarily unavailable", status=503)
    return Response("It worked this time", mimetype="text/plain")


@app.route("/trouble/flaky/reset")
def trouble_flaky_reset():
    flaky_counter["n"] = 0
    return Response("Counter reset", mimetype="text/plain")


@app.route("/trouble/agent")
def trouble_agent():
    ua = request.headers.get("User-Agent", "")
    if not ua or ua.startswith("python-requests") or ua.startswith("python-urllib"):
        return Response("<h1>403 Forbidden</h1><p>Please identify your robot.</p>",
                        status=403, mimetype="text/html")
    return Response(f"<h1>Welcome</h1><p>Your User-Agent: {ua}</p>",
                    mimetype="text/html")


@app.route("/trouble/wrong-charset")
def trouble_charset():
    body = "<h1>Café crème — prix : 3,50 €</h1>".encode("utf-8")
    return Response(body, headers={"Content-Type": "text/html; charset=ISO-8859-1"})


@app.route("/trouble/messy-cards")
def trouble_messy():
    return render_template("messy_cards.html")


# ------------------------------------------------------------------ jobs board
def jobs_on(day):
    start = BOOK_DATE
    live = []
    for j in JOBS:
        posted = start + dt.timedelta(days=j["offset"])
        if posted <= day < posted + dt.timedelta(days=j["lifetime"]):
            live.append(dict(j, posted=posted.isoformat(),
                             new=(day - posted).days < 2))
    live.sort(key=lambda j: (j["posted"], j["id"]), reverse=True)
    return live


@app.route("/jobs/")
def jobs():
    day = site_today()
    items = jobs_on(day)
    q = request.args.get("q", "").strip().lower()
    city = request.args.get("city", "")
    if q:
        items = [j for j in items if q in j["title"].lower()
                 or q in " ".join(j["skills"]).lower()]
    if city:
        items = [j for j in items if j["city"] == city]
    page = int(request.args.get("page", 1))
    pages = max(1, math.ceil(len(items) / PER_PAGE_JOBS))
    if page < 1 or page > pages:
        abort(404)
    shown = items[(page - 1) * PER_PAGE_JOBS: page * PER_PAGE_JOBS]
    cities = sorted({j["city"] for j in JOBS})
    return render_template("jobs.html", jobs=shown, page=page, pages=pages,
                           total=len(items), q=q, city=city, cities=cities, day=day)


@app.route("/jobs/<int:jid>/")
def job_detail(jid):
    day = site_today()
    for j in jobs_on(day):
        if j["id"] == jid:
            return render_template("job.html", job=j, day=day)
    abort(404)


# ------------------------------------------------------------------ price watch
def price_on(item, day):
    n = (day - BOOK_DATE).days
    wave = 0.08 * math.sin(n / 9 + item["seed"] % 7)
    drop = 0.15 if stable_unit(item["seed"], n // 7, "sale") > 0.8 else 0
    noise = (stable_unit(item["seed"], n) - 0.5) * 0.04
    return round(item["base"] * (1 + wave + noise - drop), 2)


@app.route("/prices/")
def prices():
    day = site_today()
    rows = []
    for it in WATCH:
        now, before = price_on(it, day), price_on(it, day - dt.timedelta(1))
        rows.append({"id": it["id"], "name": it["name"], "price": now,
                     "change": round(now - before, 2)})
    return render_template("prices.html", rows=rows, day=day)


@app.route("/prices/item/<int:iid>/")
def price_item(iid):
    day = site_today()
    it = next((w for w in WATCH if w["id"] == iid), None) or abort(404)
    history = [{"date": (day - dt.timedelta(d)).isoformat(),
                "price": price_on(it, day - dt.timedelta(d))} for d in range(14)]
    return render_template("price_item.html", item=it, price=history[0]["price"],
                           history=history, day=day)


@app.errorhandler(404)
def not_found(e):
    return render_template("simple.html", title="404 — Page not found",
                           text="There is no page at this address."), 404
