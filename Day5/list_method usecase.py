Pro=["Laptop","Mouse","Keyboard"]
newProd=["Monitor","Tablet","Webcam"]
count=int(input("How many product do you want to add: "))
for i in range(count):
    Pro=input("Enter pro: ")
    Pro.append(Prod)

newList=Pro + newProd
print(newList)
newList.remove("Mouse")
print(newList)
newList.remove("Webcam")
print(newList)

print(newList.count("Laptop"))
print(newList.index("Monitor"))

print(newList.sort())
print(newList[::-1])
backUp=[]
backUp=newList
print(newList)