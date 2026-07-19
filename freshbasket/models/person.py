class Person:

    def __init__(self, person_id, name, age, phone):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.phone = phone

    def __str__(self):
        return f"{self.person_id} | {self.name} | Age: {self.age} | Phone: {self.phone}"