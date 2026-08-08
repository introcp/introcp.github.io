class Person:
	age = 10
	def greet(self):
		print("Hello")

###############

class Person:
	def __init__(self, firstName, lastName, age=None, address=None):
		self.first_name = firstName
		self.last_name = lastName
		self.address = address
		self.age = age
	def greet(self):
		print("Hello!")
		print("My name is", self.first_name, self.last_name)
		print("I am", self.age, "years old")
		print("I live in", self.address)

person1 = Person("Alessio", "Martino", 30, "Viale Romania")
person2 = Person("Giorgio", "Piccardo")

person1.greet()
person2.greet()

##################################

class Dog:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	def description(self):
		return self.name + " is " + str(self.age) + " years old"
	def speak(self, sound):
		return self.name + " says " + sound

miles = Dog("Miles", 4)
print(miles.description())
print(miles.speak("Woof Woof"))
print(miles.speak("Bow Wow"))

##################################

class Counter:
	def __init__(self):
		self._count = 0
	def increase(self):
		self._count += 1
	def get_count(self):
		return self._count 

c = Counter()
c.increase()
c.increase()
print(c.get_count())


##################################

class Student(Person):
	# def __init__(self):
	# 	self.exam_grades = []
	# def add_exam(self, grade):
	# 	self.exam_grades.append(grade)
	pass

student1 = Student("Alessio", "Martino", 30, "Viale Romania")
print(student1.last_name)
student1.greet()
print(type(student1))

##################################

class Student(Person):
	def __init__(self,name,surname,uni,studID,age=None,addr=None):
		Person.__init__(self,name,surname,age,addr)
		self.university = uni
		self.studentID = studID
		self.exam_grades = []
	def add_exam(self,grade):
		self.exam_grades.append(grade)
	def get_average(self):
		return sum(self.exam_grades)/len(self.exam_grades)

student1 = Student("Alessio", "Martino", "LUISS", "123456", 30, "Viale Romania")
#
print(student1.last_name)
student1.greet()
#
student1.add_exam(30)
student1.add_exam(25)
student1.add_exam(18)
print(student1.get_average())

##################################

class Student(Person):
	def __init__(self,name,surname,uni,studID,age=None,addr=None):
		Person.__init__(self,name,surname,age,addr)
		self.university = uni
		self.studentID = studID
		self.exam_grades = []
	def add_exam(self,grade):
		self.exam_grades.append(grade)
	def get_average(self):
		return sum(self.exam_grades)/len(self.exam_grades)
	def greet(self):
		print("Hello!")
		print("My name is", self.first_name, self.last_name)
		print("I am a student at", self.university)
		print("My average grade is", self.get_average())


student1 = Student("Alessio", "Martino", "LUISS", "123456", 30, "Viale Romania")
student1.add_exam(30)
student1.add_exam(25)
student1.add_exam(18)
student1.greet()

###################################

person1 = Person("Giorgio", "Piccardo")
list_of_persons = [student1, parent1]
for item in list_of_persons:
	item.greet()