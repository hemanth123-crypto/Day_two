cate = {
    "Electronics" : {"Phone":1, "Laptop":2},
    "Snacks" : {}
}



def update():
    cat = input("Enter category: ")
    prod = input("Enter product: ")
    count = int(input("Enter the number of stock available: "))
    try:
        cate[cat].update({prod:count})
    except:
        cate[cat] = {}
        cate[cat].update({prod:count})
    return None


def inventory():
    for i,j in cate.items():
        print("\n============ Category: "+i+" ============\n")
        for k,l in cate[i].items():
            print(k+': ',l)
    return None


while(True):

    ch = int(input("Menu\n1. Update\n2. View Inventory\nYour Choice: "))

    if(ch==1):
        update()

    elif(ch==2):
        inventory()

    else:
        break