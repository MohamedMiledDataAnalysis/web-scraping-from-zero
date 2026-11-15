r"""Exercise 14.3 (medium).

    Ask for the station `XYZ`, then for an end date before the start date. Print the status code and the API's error message for each.

Expected output: chapters/ch14/expected/ex3_errors.txt
Solution: chapters/ch14/solutions/ex3_errors.py
"""
import requests
url = "http://localhost:8000/api/v1/observations"
headers = {"X-API-Key": "pg-demo-2027"}

# Your code here
