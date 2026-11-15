prices = [26.93, 19.2, 6.56, 59.27]
for price in prices:
    if price < 10:
        print(price, "cheap")
    elif price < 30:
        print(price, "normal")
    else:
        print(price, "expensive")
