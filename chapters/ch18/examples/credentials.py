import os
import sys

username = os.environ.get("PG_USER", "reader")        # demo defaults: public account
password = os.environ.get("PG_PASSWORD", "practice")
if not username or not password:
    sys.exit("Set PG_USER and PG_PASSWORD before running this script.")
print("Logging in as", username)
