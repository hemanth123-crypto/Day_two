from data.datastore import DATASTORE

from models.customer import Customer

from models.membership import (
    SilverMembership,
    GoldMembership,
    PremiumMembership
)


def load_seed_data():

    customer1 = Customer(
        1,
        "CUS01",
        "Anita",
        24,
        "9876543210",
        "anita@gmail.com",
        3000
    )

    customer2 = Customer(
        2,
        "CUS02",
        "Rahul",
        32,
        "9876543211",
        "rahul@gmail.com",
        5000
    )

    customer3 = Customer(
        3,
        "CUS03",
        "Kavin",
        16,
        "9876543212",
        "kavin@gmail.com",
        700
    )

    DATASTORE["customers"][customer1.customer_id] = customer1
    DATASTORE["customers"][customer2.customer_id] = customer2
    DATASTORE["customers"][customer3.customer_id] = customer3

    silver = SilverMembership("Silver", 200)
    gold = GoldMembership("Gold", 500)
    premium = PremiumMembership("Premium", 800)

    DATASTORE["memberships"][silver.membership_id] = silver
    DATASTORE["memberships"][gold.membership_id] = gold
    DATASTORE["memberships"][premium.membership_id] = premium