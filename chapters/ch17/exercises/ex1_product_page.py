"""Exercise 17.1 (easy).

    Open `http://localhost:8000/shop/product/42`, wait for the name, and print the name, price and stock text.

Expected output: chapters/ch17/expected/ex1_product_page.txt
Solution: chapters/ch17/solutions/ex1_product_page.py
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Your code here
