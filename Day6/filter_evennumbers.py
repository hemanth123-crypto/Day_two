number=list(map(int,input("enter numbers separated by space:").split()))

even_numbers = list(filter(lambda x: x % 2 == 0, number))

squared_evens = list(map(lambda x: x ** 2, even_numbers))

print("Squared even numbers:", squared_evens)
