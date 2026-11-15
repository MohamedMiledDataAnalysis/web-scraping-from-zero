from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("data:text/html,<title>Selenium works</title>")
print(driver.title)
driver.quit()
