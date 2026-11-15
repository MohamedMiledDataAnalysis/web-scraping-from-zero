class Counter:
    """Counts requests, per status code."""

    def __init__(self, name):
        self.name = name  # attributes: data kept in the object
        self.counts = {}

    def add(self, status):  # a method: a function of the object
        self.counts[status] = self.counts.get(status, 0) + 1

    def report(self):
        return f"{self.name}: {self.counts}"


library = Counter("library")  # create an object: calls __init__
library.add(200)
library.add(200)
library.add(404)
print(library.report())
print(library.counts[200])
