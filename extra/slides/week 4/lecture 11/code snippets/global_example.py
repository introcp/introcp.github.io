c = 0   # global variable


def add():
    global c
    c = c + 2   # increment by 2
    print("In add(): c = ", c)


add()
print("In main(): c = ", c)
