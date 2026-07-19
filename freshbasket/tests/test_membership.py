import unittest

from models.membership import (
    SilverMembership,
    GoldMembership,
    PremiumMembership
)


class TestMembership(unittest.TestCase):

    def setUp(self):

        self.silver = SilverMembership(
            "Silver",
            200
        )

        self.gold = GoldMembership(
            "Gold",
            500
        )

        self.premium = PremiumMembership(
            "Premium",
            800
        )

    def test_silver_fee(self):

        self.assertEqual(
            self.silver.calculate_fee(3),
            600
        )

    def test_gold_fee(self):

        amount = self.gold.calculate_fee(2)

        expected = (500 * 2) + ((500 * 2) * 0.18) + 200

        self.assertEqual(
            amount,
            expected
        )

    def test_premium_fee(self):

        amount = self.premium.calculate_fee(2)

        expected = (800 * 2) + 500 + 300

        self.assertEqual(
            amount,
            expected
        )

    def test_operator_equal(self):

        another = SilverMembership(
            "Silver",
            200
        )

        self.assertTrue(
            self.silver == another
        )

    def test_operator_less_than(self):

        self.assertTrue(
            self.silver < self.gold
        )

    def test_invalid_fee(self):

        with self.assertRaises(ValueError):

            SilverMembership(
                "Silver",
                -100
            )


if __name__ == "__main__":
    unittest.main()