class Car:
    def __init__(self,brand, model, year, owner):
        self.brand=brand
        self.model=model
        self.year=year
        self.__owner=owner

    def start_engine(self):
        print(f"The engine of the {self.brand} {self.model} is starting.")

    def show_info(self):
        print(f"Car Info: {self.year} {self.brand}  {self.model}")

    def set_owner(self,owner):
        if not self.__owner:
            self.__owner=owner
    def get_owner(self):
        return self.__owner

car1=Car("Toyota","Camry",2020)
car2=Car("Honda","Civic",2019)
print(car1.brand)
print(car1.__owner)

car1.set_owner("Alice")
print(car1.get_owner())

car1.start_engine()
car1.show_info()

car2.start_engine()
car2.show_info()

car=[car1,car2]
for car in cars:
    car.start_engine()
    car.show_info()
