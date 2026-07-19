from data.datastore import DATASTORE
from models.customer import Customer


class CustomerService:

    @staticmethod
    def add_customer():

        person_id = int(input("Enter Person ID : "))
        customer_id = input("Enter Customer ID : ")

        if customer_id in DATASTORE["customers"]:
            print("Customer already exists.")
            return

        name = input("Enter Name : ")
        age = int(input("Enter Age : "))
        phone = input("Enter Phone : ")
        email = input("Enter Email : ")
        wallet = float(input("Enter Wallet Amount : "))

        customer = Customer(
            person_id,
            customer_id,
            name,
            age,
            phone,
            email,
            wallet
        )

        DATASTORE["customers"][customer_id] = customer

        print("Customer Added Successfully.")

    @staticmethod
    def view_customers():

        if not DATASTORE["customers"]:
            print("No Customers Found")
            return

        for customer in DATASTORE["customers"].values():
            print(customer)

    @staticmethod
    def update_customer():

        customer_id = input("Enter Customer ID : ")

        if customer_id not in DATASTORE["customers"]:
            print("Customer Not Found")
            return

        customer = DATASTORE["customers"][customer_id]

        customer.name = input("Enter New Name : ")
        customer.phone = input("Enter New Phone : ")
        customer.email = input("Enter New Email : ")

        print("Customer Updated Successfully")

    @staticmethod
    def delete_customer():

        customer_id = input("Enter Customer ID : ")

        if customer_id in DATASTORE["customers"]:

            del DATASTORE["customers"][customer_id]

            print("Customer Deleted Successfully")

        else:
            print("Customer Not Found")