from car import Car
from ev import EV
car1=Car("Toyota","Camry",2020)
ev1=Ev("Honda","Civic",2019,75)


car1.set_owner("Alice")
print(car1.get_owner())

car1.start_engine()
car1.show_info()

ev1.start_engine()
ev1.show_info()
ev1.charge_battery()

car=[car1,car2]
for car in cars:
    car.start_engine()
    car.show_info()
