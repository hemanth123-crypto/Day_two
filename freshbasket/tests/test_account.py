import unittest

from models.customer import Customer

from models.membership import SilverMembership

from models.account import Account

from utils.validator import is_eligible


class TestAccount(unittest.TestCase):

    def setUp(self):

        self.customer = Customer(
            1,
            "CUS01",
            "Anita",
            24,
            "9999999999",
            "anita@gmail.com",
            3000
        )

        self.child = Customer(
            2,
            "CUS02",
            "Kavin",
            16,
            "8888888888",
            "kavin@gmail.com",
            700
        )

        self.membership = SilverMembership(
            "Silver",
            200
        )

    def test_account_creation(self):

        amount = self.membership.calculate_fee(3)

        account = Account(
            "ACC101",
            self.customer,
            self.membership,
            3,
            amount
        )

        self.assertEqual(
            account.status,
            "ACTIVE"
        )

        self.assertEqual(
            account.amount_paid,
            600
        )

    def test_under_age_customer(self):

        self.assertFalse(
            is_eligible(self.child)
        )

    def test_eligible_customer(self):

        self.assertTrue(
            is_eligible(self.customer)
        )

    def test_wallet_purchase(self):

        result = self.customer.purchase(500)

        self.assertTrue(result)

        self.assertEqual(
            self.customer.wallet,
            2500
        )


if __name__ == "__main__":
    unittest.main()