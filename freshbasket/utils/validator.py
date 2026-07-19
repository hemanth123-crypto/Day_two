def is_eligible(customer):
    return customer.age >= 18


def positive_integer(value):
    return value > 0


def has_active_membership(customer, datastore):

    for account in datastore["accounts"].values():

        if account.customer.customer_id == customer.customer_id:

            if account.status == "ACTIVE":
                return True

    return False