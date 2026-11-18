# Chapter 17 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 17.1 (easy)

> Open `http://localhost:8000/shop/product/42`, wait for the name, and print the name, price and stock text. Expected output:

**What the question asks.** Exercise 16.3 in Selenium: open a product page built by JavaScript, wait for the name, and read name, price and stock.

**The plan.** Start Chrome without a window, open the page, wait explicitly for `h1.name` with `WebDriverWait`, then read the two other elements, which appear at the same time. Close the browser in `finally`, whatever happens.

```python
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
```

Output:

```text
Compact Notebook £124.17 In stock
```

**Line by line.**

- `options.add_argument("--headless=new")` runs Chrome without a window; `webdriver.Chrome(options=options)` starts it.
- `try: ... finally: driver.quit()` guarantees the browser is closed, even if a line inside raises an error.
- `WebDriverWait(driver, 10).until(...)` checks the condition again and again, for up to 10 seconds.
- `EC.presence_of_element_located((By.CSS_SELECTOR, "h1.name"))` is the condition: an element matching the selector exists. Note the double brackets: the locator is one pair, `(By.CSS_SELECTOR, "h1.name")`.
- `until(...)` returns the element it waited for, so `.text` reads its text at once.
- `driver.find_element(By.CSS_SELECTOR, ...)` looks **once**, without waiting; it is safe here because the price and stock are written in the same step as the name.

**Reading the result.** `Compact Notebook £124.17 In stock`: the same line as exercise 16.3. Two tools, one page, one answer.

**Checking.** Print `driver.find_element(By.ID, "product").text`: the whole block, name, SKU, price, rating and stock.

**Mistakes this exercise provokes.**

- `driver.find_element` without the explicit wait: it looks once and raises `NoSuchElementException` if JavaScript has not finished. On a fast machine it may pass, which is worse: the program fails only sometimes.
- `presence_of_element_located(By.CSS_SELECTOR, "h1.name")` with single brackets: `TypeError`, because the condition expects one locator tuple.
- Forgetting `driver.quit()`: Chrome processes stay alive in the background after the program ends.

**The choice it makes.** Selenium waits only when you ask it to; Playwright's locators wait by default. That is the main practical difference between the two for pages like this one.

**Another way to solve it.** `visibility_of_element_located` waits until the element is not only present but displayed, which is closer to what a person sees:

```python
name = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.name"))
).text
```

For this page both conditions give `Compact Notebook`. Use visibility when a page builds elements hidden and shows them later.

**A variation to try.** Open product 999, which does not exist, with a wait of 2 seconds: `WebDriverWait(driver, 2).until(...)` raises `TimeoutException`. Catch it with `from selenium.common.exceptions import TimeoutException` and print `No such product` instead of a traceback.

**If your output differs.**

1. **`TimeoutException`**: the element never appeared; open the page in a browser and check the selector.
2. **`SessionNotCreatedException`** at start-up: Chrome and its driver versions do not match; see Chapter 0's Selenium setup.
3. **A line about *Exception managing chrome*** before the output: Selenium Manager could not reach the internet to check versions; harmless when a driver is already installed.

---

## Exercise 17.2 (medium)

> In the shop, choose *Kitchen* and sort by *Rating*, and print the three best products with their rating. Expected output:

**What the question asks.** Exercise 16.2 in Selenium: choose *Kitchen* and *Rating* in the shop's menus, then read the three best products as the page shows them.

**The plan.** Wait for the first products. Use Selenium's `Select` helper on both menus. Wait until the status text contains *of 30*, which the page writes only once the final Kitchen list is drawn. Read the first three cards.

```python
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
        "Kitchen"
    )
    Select(driver.find_element(By.ID, "sort")).select_by_value("rating")
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "status"), "of 30")
    )
    for card in driver.find_elements(By.CSS_SELECTOR, "div.product")[
        :3
    ]:
        print(
            card.find_element(By.CSS_SELECTOR, "p.rating").text,
            card.find_element(By.CSS_SELECTOR, "h3").text,
        )
finally:
    driver.quit()
```

Output:

```text
4.7 / 5 Pro Kettle
4.7 / 5 Classic Kettle
4.7 / 5 Compact Blender
```

**Line by line.**

- `wait = WebDriverWait(driver, 10)` creates one waiting object to reuse.
- `Select(driver.find_element(By.ID, "category"))` wraps the `<select>` menu; `.select_by_value("Kitchen")` chooses the option whose `value` is `Kitchen`.
- The same for `sort` with the value `rating`.
- `EC.text_to_be_present_in_element((By.ID, "status"), "of 30")` waits until the status element's text contains `of 30`.
- `driver.find_elements(...)[:3]` returns a list of cards and keeps three; inside each card, `find_element` reads the rating and the name.

**Reading the result.** The same three products as exercise 16.2, all rated 4.7, *Pro Kettle* first.

**Checking.** Print `driver.find_element(By.ID, "status").text` after the wait: `Showing 12 of 30 products`. Print the option values with `[o.get_attribute("value") for o in Select(...).options]`: `['', 'Audio', 'Garden', 'Kitchen', 'Office']`.

**Mistakes this exercise provokes.**

- Waiting for `div.product` after the menus: satisfied at once by the old products.
- `select_by_value("kitchen")` in lower case: `NoSuchElementException: Cannot locate option with value: kitchen`.
- Reading the cards right after the second `select_by_value`: you may read the list before the sort was applied.

**The choice it makes.** The page sets the status to *Loading products...* as soon as a menu changes, and writes *of 30* only when the final list is drawn. Waiting for that text is the Selenium equivalent of Playwright's `expect_response`: wait for a sign that the final state is reached, not for time to pass.

**Another way to solve it.** Choose by the visible label instead of the value, as a person would read the menu:

```python
Select(driver.find_element(By.ID, "category")).select_by_visible_text("Kitchen")
Select(driver.find_element(By.ID, "sort")).select_by_visible_text("Rating")
```

The menu labels are `Newest`, `Price` and `Rating`; the values behind them are what the API receives. Use values when they are stable codes, labels when the page is translated or the values are opaque numbers.

**A variation to try.** Wait with a condition that fails, to see what a timeout looks like: `WebDriverWait(driver, 2).until(EC.text_to_be_present_in_element((By.ID, "status"), "of 31"))` raises `TimeoutException` after 2 seconds, with an almost empty message. Selenium does not tell you what it was waiting for: name your waits in comments or in your own error messages.

**If your output differs.**

1. **Products of another category**: the wait condition is too weak; it must include `of 30`.
2. **`NoSuchElementException: Cannot locate option`**: check the value's spelling and case.

---

## Exercise 17.3 (harder)

> Scroll the *Office* category until all its products are loaded and print their number and average price. Expected output:

**What the question asks.** Exercise 16.4 in Selenium: load every *Office* product by scrolling, then compute their number and average price from the page.

**The plan.** Choose the category and wait for *of 30*. Scroll in a loop with JavaScript; after each scroll, wait until there are more products than before; stop when the status says *Showing 30*, or after 20 scrolls. Read the prices and average them.

```python
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
```

Output:

```text
30 products, average £111.58
```

**Line by line.**

- `for _ in range(20):` limits the loop to 20 scrolls.
- `before = len(driver.find_elements(...))` counts the products now on the page.
- `driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")` runs JavaScript in the page: it scrolls to the bottom, which loads the next batch. Selenium has no mouse-wheel shortcut as simple as Playwright's.
- `WebDriverWait(driver, 5).until(lambda d: len(...) > before)` waits up to 5 seconds for a condition written as a Python function: the count must grow.
- The prices are read inside `try`, before `driver.quit()`; the arithmetic happens after.

**Reading the result.** `30 products, average £111.58`: the same as exercise 16.4.

**Checking.** Print the status after each scroll: *Showing 12*, *24*, then *30 of 30 products*. The `lambda` condition shows that `until` accepts any function that takes the driver and returns something true.

**Mistakes this exercise provokes.**

- `time.sleep(2)` after each scroll instead of the wait: too short on a slow machine, wasted time on a fast one.
- Reading `e.text` after `driver.quit()`: the elements belong to a closed browser, and Selenium raises an error. Read everything before quitting.
- `while True:` without a limit: if loading stops, the program never ends.

**The choice it makes.** A Python `lambda` as a wait condition makes any test possible, at the cost of readability. Here, *more products than before* is the clearest sign that a scroll worked.

**Another way to solve it.** As with exercise 16.4, the hidden API gives the same answer in one request, without a browser: `requests.get("http://localhost:8000/shop/api/products", params={"category": "Office", "per_page": 50})` returns the 30 products, whose prices average £111.58.

**A variation to try.** Write the wait as a named function instead of a `lambda`, which reads better and can be reused:

```python
def more_products_than(n):
    return lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.product")) > n

WebDriverWait(driver, 5).until(more_products_than(before))
```

**If your output differs.**

1. **`24 products`**: the loop stopped one scroll early; print the status at the end.
2. **`TimeoutException`** during the scroll loop: no new products arrived within 5 seconds; scroll the shop by hand in a browser to check that it still loads.
3. **`StaleElementReferenceException`**: you kept elements from before a reload; find them again after each wait.

---

## Exercise 17.4 (thinking)

> Take exercise 16.5 (catching the API answers). Explain why the Selenium version is harder, and which other chapter gives the same result more simply.

**What the question asks.** No code: compare catching the API answers (exercise 16.5) in Selenium with Playwright, and name the chapter that gets the same data more simply.

**The answer.** Selenium has no simple way to read the answers the page receives. Playwright's `page.on("response", ...)` gives you each response, with its address and its JSON, in one line. In Selenium you would need one of three heavy routes:

- Chrome's **performance logs**, enabled with a capability when the browser starts, then parsed as JSON messages to find the network events;
- Chrome's **DevTools protocol**, through `driver.execute_cdp_cmd`, which works only with Chrome and needs commands to fetch each response body;
- a **proxy** between the browser and the site, such as the `selenium-wire` package, which records the traffic.

Each adds setup, ties you to one browser, or adds a package to maintain.

**The simpler chapter.** Chapter 15 gives the same 30 products in one request to the hidden API, without any browser: `/shop/api/products?category=Office&per_page=50`.

**Checking your answer.** Ask what each route costs: start-up options, browser lock-in, extra packages. If the data comes from an API the page calls, the cheapest route is to call that API yourself.

**Mistakes this exercise provokes.**

- Answering *Selenium cannot do it*: it can, but not simply.
- Forgetting why Chapter 15's route is better: no browser to start, fewer requests, clean numbers.

**The choice it makes.** Choose the tool by the data, not by habit: Playwright when you must catch what a page receives, the hidden API when you can call it, Selenium when a project already uses it.

**A variation to try.** Write down, for each of the six methods of the book, how it would get the Office products: requests and BeautifulSoup (no: the products are not in the HTML), pandas `read_html` (no table), the hidden API (yes, one request), Playwright (scroll, or catch the answers), Selenium (scroll), Scrapy (request the API's JSON pages, as a spider can request any address). Compare your table with the decision chart of Chapter 7.

**If your answer differs.** Compare the reasons, not only the conclusion: the key point is that the data comes from an API, and an API you can call yourself makes the browser unnecessary.
