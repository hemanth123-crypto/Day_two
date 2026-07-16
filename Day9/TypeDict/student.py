from typing import TypedDict

class Student(TypedDict):
    name: str
    age: int
    id: int
student1: Student = {id:1, name: "John", age: 20}
student2: Student = {id: 2, name: "Jane", age: 22}

print(student1)
print(student2)


