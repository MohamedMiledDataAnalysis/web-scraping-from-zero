from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/shop/")
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.product"))
    )
    Select(
        driver.find_element(By.ID, "category")
    ).select_by_visible_text("Garden")
    Select(driver.find_element(By.ID, "sort")).select_by_visible_text(
        "Price"
    )
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "status"), "of 30")
    )
    for card in driver.find_elements(By.CSS_SELECTOR, "div.product")[
        :3
    ]:
        price = card.find_element(By.CSS_SELECTOR, "p.price").text
        name = card.find_element(By.CSS_SELECTOR, "h3.name").text
        print(price, name)
    print(driver.find_element(By.ID, "status").text)
finally:
    driver.quit()
