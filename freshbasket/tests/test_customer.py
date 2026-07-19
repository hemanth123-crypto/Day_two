import unittest

from models.customer import Customer


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.customer = Customer(
            1,
            "CUS01",
            "Anita",
            24,
            "9876543210",
            "anita@gmail.com",
            3000
        )

    def test_customer_creation(self):

        self.assertEqual(
            self.customer.customer_id,
            "CUS01"
        )

        self.assertEqual(
            self.customer.name,
            "Anita"
        )

        self.assertEqual(
            self.customer.age,
            24
        )

        self.assertEqual(
            self.customer.email,
            "anita@gmail.com"
        )

    def test_wallet_property(self):

        self.assertEqual(
            self.customer.wallet,
            3000
        )

    def test_add_money(self):

        self.customer.add_money(500)

        self.assertEqual(
            self.customer.wallet,
            3500
        )

    def test_purchase_success(self):

        result = self.customer.purchase(1000)

        self.assertTrue(result)

        self.assertEqual(
            self.customer.wallet,
            2000
        )

    def test_purchase_failure(self):

        result = self.customer.purchase(5000)

        self.assertFalse(result)

        self.assertEqual(
            self.customer.wallet,
            3000
        )


if __name__ == "__main__":
    unittest.main()