from data.seed_data import load_seed_data
from services.store_system import StoreSystem


def menu():

    print("\n========== FreshBasket Store ==========")
    print("1. Register Customer")
    print("2. View Customers")
    print("3. Update Customer")
    print("4. Delete Customer")
    print("5. Add Membership")
    print("6. View Memberships")
    print("7. Update Membership")
    print("8. Delete Membership")
    print("9. Apply Festival Discount")
    print("10. Create Membership Account")
    print("11. Renew Membership")
    print("12. Expire Membership")
    print("13. Delete Membership Account")
    print("14. View Accounts")
    print("15. Exit")


def main():

    load_seed_data()

    system = StoreSystem()

    while True:

        menu()

        choice = input("\nEnter your choice : ")

        if choice == "1":
            system.register_customer()

        elif choice == "2":
            system.view_customers()

        elif choice == "3":
            system.update_customer()

        elif choice == "4":
            system.delete_customer()

        elif choice == "5":
            system.add_membership()

        elif choice == "6":
            system.view_memberships()

        elif choice == "7":
            system.update_membership()

        elif choice == "8":
            system.delete_membership()

        elif choice == "9":
            system.apply_discount()

        elif choice == "10":
            system.create_membership_account()

        elif choice == "11":
            system.renew_membership()

        elif choice == "12":
            system.expire_membership()

        elif choice == "13":
            system.delete_membership_account()

        elif choice == "14":
            system.view_accounts()

        elif choice == "15":
            print("\nThank you for using FreshBasket.")
            break

        else:
            print("\nInvalid Choice!")


if __name__ == "__main__":
    main()