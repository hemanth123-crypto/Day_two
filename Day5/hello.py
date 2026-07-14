print("Welcome to Python core")

a=10
b=6

print(a&b)
print(a|b)
print(a^b)
print(~a)
print(a<<2)

language="Python"
print("Py in language")
print("java in language")

print(3 in (1,2,3))
 
bal=5000
amt=int(input("Enter a number"))
if amt<=bal and amt%100 ==0:
    bal-=amt
    print("withdrawl successful")
    print("remaining bal:", bal)
else:
    print("Invalid withdrawl amount")

a=int(input("Enter marks of a student"))
if a>=40:
    print("pass")
else:
    print("fail")


password=1234
at=0
while at<3:
    user=int(input("enter password"))
    if user == password:
        print("enter successfull")
        break
    else:
        at=-1
        print("wrong password")
if at==3:
   print("you have entered correct password")

list1=["m","no","i","ke"]
list2=["y","me","s","lly"]
list3=[i + j for i, j in zip(list1,list2)]
print(list3)

list1=["mike", "", "Emmo", "kelly", "", "brad"]
resList=list(filter(None,list1))
print(resList)

stores=3
days=7
for store in range(stores):
    total_sales=0
    for day in range(1,days+1):
        sale=int(input("Enter sales for today {day}: "))
        total_sales=+sale
    print(f"total sales for store {store+1}: {total_sales}")





cat = []
pro = []
num_cat = []
num_pro = []
count = 0
fir, sec, thi = map(int, input("").split())
for i in range(fir):
    product = input("Enter product name: ")
    qty = int(input("Enter quantity available: "))
    cat.append("Category 1")
    pro.append(product)
    num_cat.append(1)
    num_pro.append(qty)
for i in range(sec):
    product = input("Enter product name: ")
    qty = int(input("Enter quantity available: "))
    cat.append("Category 2")
    pro.append(product)
    num_cat.append(2)
    num_pro.append(qty)
for i in range(thi):
    product = input("Enter product name: ")
    qty = int(input("Enter quantity available: "))
    cat.append("Category 3")
    pro.append(product)
    num_cat.append(3)
    num_pro.append(qty)
for i in range(len(pro)):
    print("Category:", cat[i])
    print("Product :", pro[i])
    print("Quantity:", num_pro[i])
    print()
count = len(pro)
print("Total number of products:", count)