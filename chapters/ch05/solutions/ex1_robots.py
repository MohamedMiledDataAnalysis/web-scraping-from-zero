from urllib.robotparser import RobotFileParser

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()
for path in ["/quotes/", "/admin/", "/private/notes.html"]:
    print(
        path,
        robots.can_fetch(
            "LearningScraper", "http://localhost:8000" + path
        ),
    )
