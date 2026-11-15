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
    Select(driver.find_element(By.ID, "category")).select_by_value(
        "Office"
    )
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "status"), "of 30")
    )
    for _ in range(20):  # never more than 20 scrolls
        if "Showing 30" in driver.find_element(By.ID, "status").text:
            break
        before = len(
            driver.find_elements(By.CSS_SELECTOR, "div.product")
        )
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        WebDriverWait(driver, 5).until(
            lambda d: len(
                d.find_elements(By.CSS_SELECTOR, "div.product")
            )
            > before
        )
    prices = [
        e.text
        for e in driver.find_elements(
            By.CSS_SELECTOR, "div.product p.price"
        )
    ]
finally:
    driver.quit()
values = [float(t.replace("£", "")) for t in prices]
print(
    len(values),
    "products, average £" + f"{sum(values) / len(values):.2f}",
)
