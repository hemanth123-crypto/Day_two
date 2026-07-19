from data.datastore import DATASTORE

from models.membership import (
    SilverMembership,
    GoldMembership,
    PremiumMembership
)


class MembershipService:

    @staticmethod
    def add_membership():

        print("\n1. Silver")
        print("2. Gold")
        print("3. Premium")

        choice = input("Choose Membership : ")

        monthly_fee = float(input("Monthly Fee : "))

        if choice == "1":

            membership = SilverMembership(
                "Silver",
                monthly_fee
            )

        elif choice == "2":

            membership = GoldMembership(
                "Gold",
                monthly_fee
            )

        elif choice == "3":

            membership = PremiumMembership(
                "Premium",
                monthly_fee
            )

        else:

            print("Invalid Choice")
            return

        DATASTORE["memberships"][
            membership.membership_id
        ] = membership

        print("Membership Added Successfully")

    @staticmethod
    def view_memberships():

        if not DATASTORE["memberships"]:

            print("No Memberships Found")

            return

        for membership in DATASTORE["memberships"].values():

            print(membership)

    @staticmethod
    def update_membership():

        membership_id = input("Membership ID : ")

        if membership_id not in DATASTORE["memberships"]:

            print("Membership Not Found")

            return

        membership = DATASTORE["memberships"][
            membership_id
        ]

        membership.monthly_fee = float(
            input("Enter New Monthly Fee : ")
        )

        print("Membership Updated Successfully")

    @staticmethod
    def delete_membership():

        membership_id = input("Membership ID : ")

        if membership_id in DATASTORE["memberships"]:

            del DATASTORE["memberships"][
                membership_id
            ]

            print("Membership Deleted Successfully")

        else:

            print("Membership Not Found")

    @staticmethod
    def apply_discount():

        membership_id = input("Membership ID : ")

        if membership_id not in DATASTORE["memberships"]:

            print("Membership Not Found")

            return

        membership = DATASTORE["memberships"][
            membership_id
        ]

        setattr(
            membership,
            "festival_discount",
            10
        )

        print(
            "Festival Discount Applied :",
            getattr(
                membership,
                "festival_discount"
            ),
            "%"
        )