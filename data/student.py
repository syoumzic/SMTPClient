class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

    def __str__(self):
        return f"I am {self.name} and I study {self.major}"

student = Student("Alice", "Chemistry")
print(student)