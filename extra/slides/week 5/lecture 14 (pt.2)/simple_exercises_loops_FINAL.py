######################
# # # Exercise 1 # # #
######################

import random

head = 0
tail = 0

n = int(input("How many coin tosses? "))

for i in range(n):
    x = random.randint(1, 100)
    if x > 50:
        head = head + 1
    else:
        tail = tail + 1


print("Number of heads: ", head)
print("Number of tails: ", tail)


######################
# # # Exercise 2 # # #
######################

def rolling_sum():
    this_number = int(input("Insert a number: "))
    my_sum = this_number

    while this_number != 0:
        this_number = int(input("Insert a number: "))
        my_sum = my_sum + this_number

    return my_sum


print("Total sum is: ", rolling_sum())


######################
# # # Exercise 3 # # #
######################

def odd_or_even(n):
    odd = 0
    even = 0

    for i in range(1, n + 1):
        if i % 2 == 0:
            even += 1
        else:
            odd += 1
    print("Number of odd elements: ", odd)
    print("Number of even elements: ", even)


######################
# # # Exercise 4 # # #
######################

def fibonacci1(n):
    second_to_last = 0                  # fixed term of the sequence
    last = 1                            # fixed term of the sequence
    # we print the first seed only if n is 0
    if n == 0:
        print(second_to_last)
    # we print the first two seeds only if n is 1
    elif n == 1:
        print("%d\n%d" % (second_to_last, last))
        # print(last)
    # if n is greater than 1, we must generate new numbers
    else:
        print("%d\n%d\n" % (second_to_last, last))
        for i in range(n):
            new = last + second_to_last     # we get the new value of the Fibonacci sequence
            print(new)
            second_to_last = last           # update the last two
            last = new                      # items of the sequence


######################
# # # Exercise 5 # # #
######################

# def fibonacci2(n):
#     second_to_last = 0                  # fixed term of the sequence
#     last = 1                            # fixed term of the sequence
#
#     print(second_to_last)               # we print the fixed term for completeness
#
#     while last < n:
#         print(last)
#         new = last + second_to_last     # we get the new value of the Fibonacci sequence
#         second_to_last = last           # update the last two items of the sequence
#         last = new                      #


######################
# # # Exercise 5 # # #
######################

def multiples(n):
    for num in range(1, n + 1):
        if num % 3 == 0 and num % 5 == 0:
            print("Mult35")
        elif num % 3 == 0:
            print("Mult3")
        elif num % 5 == 0:
            print("Mult5")
        else:
            print(num)


############################################
# # # Exercise 6 [inefficient version] # # #
############################################

# def print_subset(n, m):
#     for num in range(1, n + 1):
#         if num <= m:
#             print(num)


##########################################
# # # Exercise 6 [efficient version] # # #
##########################################

def print_subset(n, m):
    for num in range(1, n + 1):
        print(num)
        if num == m:
            break


######################
# # # Exercise 7 # # #
######################
def smallerPrimes(n):
    for num in range(2, n):
        isPrime = True
        for i in range(2, round(num / 2)):
            if num % i == 0:
                isPrime = False
                break
        if isPrime:
            print(num)


######################
# # # Exercise 8 # # #
######################
def pyhtagoreanTriple(n):
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            if n**2 == x**2 + y**2:
                print(x, y)
