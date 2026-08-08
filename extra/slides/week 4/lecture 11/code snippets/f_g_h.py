def f(x):
    x = 1
    x += 1
    print(x)


def g(x):
    print(x)
    print(x + 1)


def h(y):
    x += 1


x = 5
f(x)
g(x)
h(x)
print(x)
