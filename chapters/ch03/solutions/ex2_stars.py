def stars_to_number(word):
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    return words.get(word.lower())


print(stars_to_number("Three"))
print(stars_to_number("five"))
print(stars_to_number("Six"))
