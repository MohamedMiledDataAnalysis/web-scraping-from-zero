from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/shop/")
    print("Right after get:", len(driver.find_elements(By.CSS_SELECTOR, "div.product")))
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product")))
    print("After waiting:", len(driver.find_elements(By.CSS_SELECTOR, "div.product")))
    print(driver.find_element(By.ID, "status").text)
finally:
    driver.quit()
