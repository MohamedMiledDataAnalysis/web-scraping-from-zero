"""Start the Practice Ground companion website.

    python run_site.py            the site as printed in the book (site date 2027-03-01)
    python run_site.py --live     jobs and prices follow today's date
    python run_site.py --date 2027-03-15   choose the site date yourself

Then open http://localhost:8000 in your browser. Stop the site with Ctrl+C.
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "site"))
from app import app  # noqa: E402

parser = argparse.ArgumentParser(description="Start the Practice Ground website")
parser.add_argument("--live", action="store_true", help="follow today's date")
parser.add_argument("--date", help="site date, for example 2027-03-15")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()

if args.live:
    app.config["SITE_DATE"] = "live"
elif args.date:
    app.config["SITE_DATE"] = dt.date.fromisoformat(args.date)

print(f"Practice Ground is running at http://localhost:{args.port}")
print("Leave this window open. Press Ctrl+C to stop the site.")
app.run(host="127.0.0.1", port=args.port, threaded=True)
