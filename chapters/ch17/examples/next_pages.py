from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
authors = []
try:
    driver.get("http://localhost:8000/quotes/js/")
    wait = WebDriverWait(driver, 10)
    while True:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote")))
        authors += [e.text for e in driver.find_elements(By.CSS_SELECTOR, "small.author")]
        links = driver.find_elements(By.CSS_SELECTOR, "li.next a")
        if not links:
            break
        old = driver.find_element(By.CSS_SELECTOR, "div.quote")
        links[0].click()
        wait.until(EC.staleness_of(old))
finally:
    driver.quit()
print(len(authors), "quotes; last author:", authors[-1])
