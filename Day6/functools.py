from functools import partial
multiply = lambda x, y: x * y
double = partial(multiply, 2)
print(double(5))  # Output: 10

from functools import reduce
numbers = [1, 2, 3, 4]
result = reduce(lambda x, y: x * y, numbers)
print("Product of all numbers:", result)
