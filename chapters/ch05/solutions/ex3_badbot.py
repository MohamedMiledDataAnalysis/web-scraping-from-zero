from urllib.robotparser import RobotFileParser

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()
print(robots.can_fetch("BadBot", "http://localhost:8000/library/"))
# The group "User-agent: BadBot" contains "Disallow: /",
# which forbids every address of the site to this robot.
