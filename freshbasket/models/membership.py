class Membership:

    store_name = "FreshBasket"

    id_prefix = ""

    joining_fee = 0

    counter = 100

    def __init__(self,
                 membership_name,
                 monthly_fee,
                 discount_percentage=0):

        if monthly_fee <= 0:
            raise ValueError("Monthly fee should be positive.")

        Membership.counter += 1

        self.membership_id = f"{self.id_prefix}-{Membership.counter}"

        self.membership_name = membership_name

        self.monthly_fee = monthly_fee

        self.discount_percentage = discount_percentage

    def calculate_fee(self, months):

        return self.monthly_fee * months + self.joining_fee

    def __eq__(self, other):

        return self.monthly_fee == other.monthly_fee

    def __lt__(self, other):

        return self.monthly_fee < other.monthly_fee

    def __str__(self):

        return (f"{self.membership_id} | "
                f"{self.membership_name} | "
                f"Monthly Fee : ₹{self.monthly_fee}")


class SilverMembership(Membership):

    id_prefix = "SIL"

    joining_fee = 0

    def calculate_fee(self, months):

        return self.monthly_fee * months


class GoldMembership(Membership):

    id_prefix = "GLD"

    joining_fee = 200

    def calculate_fee(self, months):

        fee = self.monthly_fee * months

        gst = fee * 0.18

        return fee + gst + self.joining_fee


class PremiumMembership(Membership):

    id_prefix = "PRE"

    joining_fee = 500

    def calculate_fee(self, months):

        gift_charge = 300

        return self.monthly_fee * months + self.joining_fee + gift_charge