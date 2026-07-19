from data.datastore import DATASTORE
from models.account import Account
from utils.validator import (
    is_eligible,
    has_active_membership
)


class AccountService:

    account_counter = 100

    @classmethod
    def create_membership(cls):

        customer_id = input("Enter Customer ID : ")

        if customer_id not in DATASTORE["customers"]:
            print("Customer Not Found")
            return

        customer = DATASTORE["customers"][customer_id]

        if not is_eligible(customer):
            print("Customer is below 18 years.")
            return

        if has_active_membership(customer, DATASTORE):
            print("Customer already has an active membership.")
            return

        print("\nAvailable Memberships")

        for membership in DATASTORE["memberships"].values():
            print(
                membership.membership_id,
                membership.membership_name,
                membership.monthly_fee
            )

        membership_id = input(
            "\nEnter Membership ID : "
        )

        if membership_id not in DATASTORE["memberships"]:
            print("Membership Not Found")
            return

        membership = DATASTORE["memberships"][
            membership_id
        ]

        months = int(
            input("Enter Number of Months : ")
        )

        amount = membership.calculate_fee(months)

        print(f"\nTotal Amount = ₹{amount}")

        if not customer.purchase(amount):
            print("Insufficient Wallet Balance")
            return

        cls.account_counter += 1

        account_id = f"ACC{cls.account_counter}"

        account = Account(
            account_id,
            customer,
            membership,
            months,
            amount
        )

        DATASTORE["accounts"][
            account_id
        ] = account

        print("\nMembership Created Successfully")
        print(account)

    @staticmethod
    def renew_membership():

        account_id = input(
            "Enter Account ID : "
        )

        if account_id not in DATASTORE["accounts"]:
            print("Account Not Found")
            return

        account = DATASTORE["accounts"][
            account_id
        ]

        months = int(
            input("Renew for Months : ")
        )

        amount = account.membership.calculate_fee(
            months
        )

        if not account.customer.purchase(amount):
            print("Insufficient Wallet")
            return

        account.months += months
        account.amount_paid += amount
        account.status = "ACTIVE"

        setattr(
            account,
            "renewal_offer",
            "5% Cashback"
        )

        print("\nRenewed Successfully")

        print(
            "Offer :",
            getattr(
                account,
                "renewal_offer"
            )
        )

    @staticmethod
    def expire_membership():

        account_id = input(
            "Enter Account ID : "
        )

        if account_id not in DATASTORE["accounts"]:
            print("Account Not Found")
            return

        account = DATASTORE["accounts"][
            account_id
        ]

        account.status = "EXPIRED"

        print("Membership Expired")

    @staticmethod
    def delete_membership():

        account_id = input(
            "Enter Account ID : "
        )

        if account_id in DATASTORE["accounts"]:

            del DATASTORE["accounts"][
                account_id
            ]

            print("Membership Deleted")

        else:

            print("Account Not Found")

    @staticmethod
    def view_accounts():

        if not DATASTORE["accounts"]:
            print("No Accounts Available")
            return

        for account in DATASTORE["accounts"].values():
            print(account)