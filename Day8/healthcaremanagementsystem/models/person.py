class Person:
    def __init__(self, name, age, id):
        self.name = name
        self.age = age
        self.id = id
    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, ID: {self.id}")
