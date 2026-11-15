from urllib.robotparser import RobotFileParser

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()

agent = "LearningScraper"
for path in ["/library/", "/private/", "/admin/login", "/jobs/"]:
    url = "http://localhost:8000" + path
    print(f"{path:<16} allowed: {robots.can_fetch(agent, url)}")

print("Crawl-delay:", robots.crawl_delay(agent))
print("Crawl-delay for SlowBot:", robots.crawl_delay("SlowBot"))
print("BadBot on /library/:", robots.can_fetch("BadBot", "http://localhost:8000/library/"))
