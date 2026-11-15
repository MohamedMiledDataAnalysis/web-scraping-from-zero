from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1200,800")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/shop/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product")))
    while True:
        count = len(driver.find_elements(By.CSS_SELECTOR, "div.product"))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 3).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.product")) > count)
        except TimeoutException:
            break
    print(len(driver.find_elements(By.CSS_SELECTOR, "div.product")), "products")
    print(driver.find_element(By.ID, "status").text)
finally:
    driver.quit()
