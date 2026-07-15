class UserAuth:

    def __init__(self):
        self.users = {"admin": "admin123"}

    def register(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False

        self.users[username] = password
        print("Registration Successful!")
        return True

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            print("Login Successful!")
            return True

        print("Invalid Username or Password.")
        return False

    def display_users(self):
        print("\nRegistered Users:")
        print(self.users)


def main():
    auth = UserAuth()

    while True:

        print("\n===== User Authentication =====")
        print("1. Register")
        print("2. Login")
        print("3. Display Users")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            auth.register(username, password)

        elif choice == "2":
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            auth.login(username, password)

        elif choice == "3":
            auth.display_users()

        elif choice == "4":
            print("Thank You!")
            break

        else:
            print("Invalid Choice.")


if __name__ == "__main__":
    main()