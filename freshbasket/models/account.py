class Account:

    def __init__(self,
                 account_id,
                 customer,
                 membership,
                 months,
                 amount_paid):

        self.account_id = account_id

        self.customer = customer

        self.membership = membership

        self.months = months

        self.amount_paid = amount_paid

        self.status = "ACTIVE"

    def expire(self):

        self.status = "EXPIRED"

    def __str__(self):

        offer = getattr(self, "renewal_offer", "No Offer")

        return (
            f"\nAccount ID : {self.account_id}\n"
            f"Customer   : {self.customer.name}\n"
            f"Membership : {self.membership.membership_name}\n"
            f"Months     : {self.months}\n"
            f"Amount     : ₹{self.amount_paid}\n"
            f"Status     : {self.status}\n"
            f"Offer      : {offer}\n"
        )

    def __del__(self):

        print("[ARCHIVED] Membership Closed")