from bs4 import BeautifulSoup

html = '<ul id="menu"><li><a href="/library/">Library</a></li>' \
       '<li class="active"><a href="/quotes/">Quotes</a></li></ul>'
soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())
