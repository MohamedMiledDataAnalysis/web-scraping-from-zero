r"""Exercise 5.4 (harder).

    Change `polite_get` so it also refuses to run when the response status is 429, 403 or 401, printing `Stopping: status 403` (for example) and returning `None`. Test it on `/library/` and `/trouble/status/403`.

Expected output: chapters/ch05/expected/ex4_polite_stop.txt
Solution: chapters/ch05/solutions/ex4_polite_stop.py
"""
import time
from urllib.robotparser import RobotFileParser
import requests
AGENT = "LearningScraper/1.0 (+mailto:reader@example.com)"
BASE = "http://localhost:8000"

# Your code here
