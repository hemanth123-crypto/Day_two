class Overloadingdemo:
    def show_details(self,*args):
        if len(args)==1:
            print(f"Car Brand:{args[0]}")
        elif len(args)==2:
            print(f"Car brand:{args[0]},model:{args[1]}")
        elif len(args)==3:
            print(f"Car brand:{args[0]},model:{args[1]},year:{args[2]}")
        else:
            print("Invalid number od arguments.please provide 1 to 3 arguments.")
def Overloading_demo():
    demo=Overloadingdemo()
    demo.show_details("Toyota")
    demo.show_details("Honda","Civic")
    demo.show_details("Ford","Mustang",2020)
    demo.show_details("chevrolet","camaro",2021,"extra argument")