import os
import sys

# For the practice account only: real scripts must not set defaults.
os.environ.setdefault("PG_USER", "reader")
os.environ.setdefault("PG_PASSWORD", "practice")

username = os.environ.get("PG_USER")
password = os.environ.get("PG_PASSWORD")
if not username or not password:
    sys.exit("Set PG_USER and PG_PASSWORD before running this script.")
print("Logging in as", username)
