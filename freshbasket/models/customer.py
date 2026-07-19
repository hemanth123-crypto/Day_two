from models.person import Person


class Customer(Person):

    def __init__(self,
                 person_id,
                 customer_id,
                 name,
                 age,
                 phone,
                 email,
                 wallet):

        super().__init__(person_id, name, age, phone)

        self.customer_id = customer_id
        self.email = email
        self.__wallet = wallet

    @property
    def wallet(self):
        return self.__wallet

    def add_money(self, amount):
        if amount > 0:
            self.__wallet += amount

    def purchase(self, amount):

        if amount <= self.__wallet:
            self.__wallet -= amount
            return True

        return False

    def __str__(self):

        return (f"{self.customer_id} | "
                f"{self.name} | "
                f"{self.age} | "
                f"{self.email} | "
                f"Wallet: ₹{self.wallet}")