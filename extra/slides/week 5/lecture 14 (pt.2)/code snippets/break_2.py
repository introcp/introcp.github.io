mysum = 0

for i in range(30):
    for n in range(20):
        if n > 2:
            break
        mysum += i
    if i > 1:
        break
    print("mysum = ", mysum)

print(mysum)
