from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

out = Path("output/ch17")
out.mkdir(parents=True, exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/shop/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.product")))
    driver.save_screenshot(str(out / "shop.png"))
    html = driver.page_source
finally:
    driver.quit()
soup = BeautifulSoup(html, "html.parser")
print(len(soup.select("div.product")), "products in the final HTML")
print((out / "shop.png").exists())
