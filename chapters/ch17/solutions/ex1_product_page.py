from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/shop/product/42")
    name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.name"))).text
    price = driver.find_element(By.CSS_SELECTOR, "#product p.price").text
    stock = driver.find_element(By.CSS_SELECTOR, "#product p.stock").text
    print(name, price, stock)
finally:
    driver.quit()
