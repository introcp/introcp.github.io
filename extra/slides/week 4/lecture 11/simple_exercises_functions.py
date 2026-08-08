#####################
### Exercise 1 v1 ###
#####################
# Write a Python function that takes the maximum of three numbers [naiive version]

def max_of_three(x, y, z):
    if x > y and x > z:
        return x
    if y > x and y > z:
        return y
    if z > y and z > x:
        return z


print(max_of_three(4, 7, 1))


#####################
### Exercise 1 v2 ###
#####################
# Write a Python function that takes the maximum of three numbers [nested version]

def max_of_two(x, y):
    if x > y:
        return x
    else:
        return y


def max_of_three(x, y, z):
    return max_of_two(x, max_of_two(y, z))


print(max_of_three(4, 7, 1))


##################
### Exercise 2 ###
##################
# Write a Python function that checks violations of the Fermat's Last Theorem.
# The theorem says that there are no positive integers a, b, c, n such that a^n + b^n = c^n for any n greater that 2.
# If n is greater than 2 and a^n + b^n = c^n, the function should return "Fermat was wrong!”, otherwise it should return "Fermat was right!”

def check_fermat(a, b, c, n):
    # inputs must be positive
    if a <= 0 or b <= 0 or c <= 0 or n <= 0:
        return "Inputs must be positive"
    # check Fermat
    if n > 2:
        if a**n + b**n == c**n:
            return "Fermat was wrong!"
        else:
            return "Fermat was right!"
    else:
        return "n must be greater than 2."


##################
### Exercise 3 ###
##################
# Write a function that prompts the user to input values for a, b, c and n, converts them to
# integers, and uses check_fermat to check whether they violate Fermat’s theorem.

def fermat_input():
    a = int(input("Enter integer variable a: "))
    b = int(input("Enter integer variable b: "))
    c = int(input("Enter integer variable c: "))
    n = int(input("Enter integer exponent n: "))
    print(check_fermat(a, b, c, n))


fermat_input()
