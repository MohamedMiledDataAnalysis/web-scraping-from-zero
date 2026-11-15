from bs4 import BeautifulSoup

html = """<div class="quote">
  <span class="text">“Tidy the desk.”</span>
  <span class="by">by <small class="author">Ada Fernhill</small></span>
</div>"""
soup = BeautifulSoup(html, "html.parser")
by = soup.find("span", class_="by")
print(repr(by.text))
print(repr(by.get_text(strip=True)))
print(repr(soup.div.get_text(" ", strip=True)))
print(repr(soup.find("span", class_="text").text.strip("“”")))
