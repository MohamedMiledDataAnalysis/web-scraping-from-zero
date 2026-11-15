from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/quotes/js/")
    quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote span.text")
    print(len(quotes), "quotes")
    print(quotes[0].text)
finally:
    driver.quit()
