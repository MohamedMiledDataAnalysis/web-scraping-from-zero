"""Exercise 4.2 (easy).

    The last page of the History category has the address `http://localhost:8000/library/category/history/page-3.html`. Use `urljoin` to compute where these links lead from it: `page-2.html`, `../fiction/`, `/library/book/salt-kingdom-2.html`.

Expected output: chapters/ch04/expected/ex2_urljoin.txt
Solution: chapters/ch04/solutions/ex2_urljoin.py
"""
from urllib.parse import urljoin
base = "http://localhost:8000/library/category/history/page-3.html"

# Your code here
