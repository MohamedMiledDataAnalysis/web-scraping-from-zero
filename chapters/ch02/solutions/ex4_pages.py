for page in range(48, 51):
    print(f"http://localhost:8000/library/page-{page}.html")

even = [f"page-{n}.html" for n in range(2, 11, 2)]
print(" ".join(even))
