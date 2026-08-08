def countdown(n):
	if n == 0:
		print("Blastoff!")
	else:
		print(n)
		countdown(n-1)

countdown(3)

##############################

def factorial(n):
	if n == 0:
		return 1
	else:
		return n * factorial(n-1)

result = factorial(5)
print(result)

##############################

def fibonacci(n):
	if n in [0, 1]:
		return n
	else:
		return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(4))

##############################

def palindrome(s):
	if len(s) <= 1:
		return True
	else:
		return s[0] == s[-1] and palindrome(s[1:-1])

print(palindrome("racecar"))
print(palindrome("rediviuer"))