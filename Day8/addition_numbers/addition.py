def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

def main():
    print("===============Simple Calculator===============")
    print("1.Addition")
    print("2.Subtraction")
    print("3.Multiplication")
    print("4.Division")

    choicel=int(input("Enter your choice: 1.Addition 2.Subtraction 3.Multiplication 4.Division"))
    num1=int(input("Enter first number"))
    num2=int(input("Enter second number"))

    if choicel==1:
        print("Addition:", add(num1, num2))
    elif choicel==2:
        print("Subtraction:", subtract(num1, num2)) 
    elif choicel==3:
        print("Multiplication:", multiply(num1, num2))      
    elif choicel==4:
        if num2==0:
            print("Division by zero is not allowed.")
        else:
            print("Division:", divide(num1, num2))  
    else:
        print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()