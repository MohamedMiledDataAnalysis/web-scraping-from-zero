# Glossary

**API (Application Programming Interface).** A door a website opens for programs, answering with data (usually JSON) instead of pages. Chapter 14.

**Attribute.** A `name="value"` pair inside an HTML tag, such as `href` or `class`.

**Backoff (exponential).** Waiting longer after each failure: 1, 2, 4, 8 seconds. Chapter 20.

**BeautifulSoup.** The Python package that turns HTML into a searchable tree. Chapter 9.

**Browser automation.** Driving a real browser from code, with Playwright or Selenium. Chapters 16 and 17.

**Cache.** A saved copy of a downloaded page, used instead of downloading it again. Chapter 8.

**Class.** A name in an element's `class` attribute; one element can have several: `class="star-rating Three"`. Chapter 4.

**Cookie.** A small value a website asks your client to send back with every request; it keeps you logged in. Chapter 18.

**Crawl.** Visiting many pages by following links.

**Crawl-delay.** A robots.txt line asking robots to wait between requests. Chapter 5.

**CSRF token.** A random value in a form that the server checks, to make sure the form was sent from its own page. Chapter 18.

**CSS selector.** A short text that describes elements: `article.book-card p.price`. Chapter 10.

**CSV.** A table saved as text, one line per row, columns separated by commas (or semicolons).

**DataFrame.** pandas' table: rows, named columns, one type per column. Chapter 7.

**Data attribute.** An attribute whose name starts with `data-`, holding a value for the page's JavaScript: `data-id="17"`. Chapter 4.

**Data dictionary.** A document listing a dataset's columns, types, units and sources. Chapter 26.

**Database right.** In the UK and the EU, the protection of a database that needed substantial investment. Chapter 5.

**Developer tools.** The browser's panels for inspecting a page: Elements, Network, Console. Chapter 4.

**DOM.** The tree the browser builds from the HTML: repaired and completed by the browser, then changed by JavaScript. Chapter 4.

**Element.** An opening tag, its content and its closing tag: `<p class="price">£26.93</p>`. Chapter 4.

**Encoding.** The rule that turns bytes into characters: UTF-8, UTF-16, ISO-8859-1. Chapters 8 and 19.

**Endpoint.** One address of an API, such as `/api/v1/stations`.

**Environment variable.** A named value the terminal gives to programs; the place for keys and passwords. Chapter 14.

**Exit code.** The number a program returns when it ends: 0 for success. Chapter 22.

**Headless.** A browser running without a window.

**Header (HTTP).** A line of information sent with a request or a response, such as `User-Agent` or `Content-Type`.

**Hidden API.** The JSON address a page's own JavaScript calls, found in the Network panel. Chapter 15.

**HTML.** The language of web pages: tags, attributes and text, nested in a tree.

**HTTP.** The protocol of requests and responses between clients and websites.

**id.** An attribute naming one unique element of the page: `id="description"`. Chapter 4.

**Idempotent.** Giving the same result when run twice; required for scheduled jobs. Chapter 22.

**Infinite scroll.** A page that loads more content when you reach its bottom. Chapter 16.

**Item (Scrapy).** One result yielded by a spider. Chapter 21.

**JSON.** A text format for nested data, like Python's dictionaries and lists. Chapter 3.

**JSON-LD.** Structured data inside a `script` tag, following schema.org, made for search engines. Chapter 11.

**Licence.** The conditions under which data may be reused: OGL, Licence Ouverte, CC BY, CC BY-SA, CC BY-NC. Chapter 5.

**Locator (Playwright).** A description of elements that waits for them when you act. Chapter 16.

**Log.** Time-stamped messages a program writes, at levels from DEBUG to CRITICAL. Chapter 20.

**Pagination.** Results split over several pages, with *next* links or page numbers. Chapter 12.

**Parser.** The program that reads HTML into a tree: `html.parser`, `lxml`. Chapter 9.

**Personal data.** Any information about an identifiable person. Chapter 5.

**Pipeline (Scrapy).** A class that cleans, checks or stores every item. Chapter 21.

**Practice Ground.** The book's companion website, run on your computer with `python run_site.py`.

**Query string.** The part of a URL after `?`: `q=python&page=2`.

**Rate limit.** The maximum number of requests a site or API accepts in a period. Chapters 14 and 20.

**Regular expression.** A pattern for text: `\d+`, `[\d,]+`. Chapters 7 and 13.

**Relative link.** A link that gives only part of the address; completed with `urljoin`. Chapter 4.

**Retry-After.** A response header giving the number of seconds to wait before trying again. Chapter 20.

**robots.txt.** The file in which a site's owner tells robots which pages they may visit. Chapter 5.

**schema.org.** The shared vocabulary of JSON-LD: `Book`, `Product`, `JobPosting`. Chapter 11.

**Scrapy.** The Python framework for large and repeated crawls. Chapter 21.

**Session.** A `requests.Session` that keeps settings, connections and cookies between requests. Chapters 8 and 18.

**Source (page source).** The HTML exactly as the website sends it; Ctrl+U in the browser. Chapter 4.

**Spider.** A Scrapy class that says where to start and what to extract. Chapter 21.

**SQLite.** A database in one file, built into Python. Chapters 13, 22, 24 and 25.

**Status code.** The three-digit number of a response: 200, 301, 404, 429, 503. Chapter 4.

**Tag.** The markup that opens or closes an element: `<p>`, `</p>`. Chapter 4.

**Terms of use.** A website's conditions; they can forbid robots and reuse. Chapter 5.

**Timeout.** The number of seconds a request waits for an answer before giving up. Chapter 8.

**URL.** A web address: scheme, host, port, path, query string, fragment. Chapter 4.

**User-Agent.** The header in which a client names itself; your scraper's name and contact. Chapters 5 and 8.

**Virtual environment.** A private copy of Python for one project, in `.venv`. Chapter 0.

**XPath.** A language for finding elements, strong on text and ancestors. Chapter 10.

```{=latex}
\setcounter{secnumdepth}{1}
```
